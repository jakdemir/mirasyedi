from typing import Dict, List, Optional
from .models import Estate, FamilyTree, FamilyNode, Person, ParentType

class InheritanceResult:
    def __init__(self):
        self.total_distributed: float = 0

class InheritanceCalculator:
    def __init__(self, estate: Estate):
        self.estate = estate
        self.family_tree = estate.family_tree
        self.total_value = estate.total_value
        self.result = InheritanceResult()

    def calculate(self) -> InheritanceResult:
        """Calculate inheritance shares for all heirs"""
        root = self.family_tree.root
        
        # Reset all shares
        self._reset_shares(root)
        
        # Determine inheritance degree and distribute accordingly
        if self._has_first_degree_heirs(root):
            self._distribute_first_degree(root)
        elif self._has_second_degree_heirs(root):
            self._distribute_second_degree(root)
        elif self._has_third_degree_heirs(root):
            self._distribute_third_degree(root)
        else:
            # If no heirs except spouse, spouse gets everything
            if root.spouse and root.spouse.is_alive:
                root.spouse.share = self.total_value
                self.result.total_distributed = self.total_value
        
        return self.result

    def _reset_shares(self, node: FamilyNode):
        """Reset all shares to 0"""
        if node.person:
            node.person.share = 0
        if node.spouse:
            node.spouse.share = 0
        for child in node.children:
            self._reset_shares(child)
        if node.parents:
            for parent in node.parents.values():
                if parent:
                    self._reset_shares(parent)

    def _has_first_degree_heirs(self, root: FamilyNode) -> bool:
        """Check if there are any living children or their descendants"""
        return any(self._has_living_descendants(child) for child in root.children)

    def _has_second_degree_heirs(self, root: FamilyNode) -> bool:
        """Check if there are any living parents or siblings"""
        if not root.parents:
            return False
        
        for parent_node in root.parents.values():
            if parent_node:
                if parent_node.person and parent_node.person.is_alive:
                    return True
                for sibling in parent_node.children:
                    if sibling.person.id != root.person.id and self._has_living_descendants(sibling):
                        return True
        return False

    def _has_third_degree_heirs(self, root: FamilyNode) -> bool:
        """Check if there are any living grandparents or uncles/aunts"""
        if not root.parents:
            return False

        for parent_node in root.parents.values():
            if not parent_node or not parent_node.parents:
                continue
            
            for grandparent in parent_node.parents.values():
                if grandparent:
                    if grandparent.person and grandparent.person.is_alive:
                        return True
                    # Only check for living uncles/aunts, not their descendants
                    for uncle in grandparent.children:
                        if (uncle.person and uncle.person.is_alive and 
                            uncle.person.id != parent_node.person.id):
                            return True
        return False

    def _has_living_descendants(self, node: FamilyNode) -> bool:
        """Check if a node has any living descendants"""
        if node.person and node.person.is_alive:
            return True
        return any(self._has_living_descendants(child) for child in node.children)

    def _distribute_first_degree(self, root: FamilyNode):
        """Distribute inheritance to first degree heirs (spouse and children)"""
        spouse_share = 0.25 if root.spouse and root.spouse.is_alive else 0

        if spouse_share > 0:
            root.spouse.share = round(self.total_value * spouse_share)
            self.result.total_distributed += root.spouse.share

        remaining_amount = self.total_value - self.result.total_distributed

        # Get all valid branches (living children or deceased with heirs)
        valid_branches = []
        for child in root.children:
            if child.person.is_alive:
                valid_branches.append(child)
            elif self._has_living_descendants(child):
                valid_branches.append(child)

        if valid_branches:
            share_per_branch = remaining_amount / len(valid_branches)
            total_distributed = 0

            for i, branch in enumerate(valid_branches):
                # Last branch gets the remainder to ensure total is exact
                if i == len(valid_branches) - 1:
                    branch_amount = remaining_amount - total_distributed
                else:
                    branch_amount = round(share_per_branch)
                    total_distributed += branch_amount

                if branch.person.is_alive:
                    branch.person.share = branch_amount
                    self.result.total_distributed += branch_amount
                else:
                    self._distribute_to_children(branch.children, branch_amount)

    def _distribute_to_children(self, children: List[FamilyNode], amount: float):
        """Distribute amount equally among children or their descendants"""
        valid_children = []
        for child in children:
            if child.person.is_alive:
                valid_children.append(child)
            elif self._has_living_descendants(child):
                valid_children.append(child)

        if not valid_children:
            return

        share_per_child = amount / len(valid_children)
        total_distributed = 0

        for i, child in enumerate(valid_children):
            # Last child gets the remainder to ensure total is exact
            if i == len(valid_children) - 1:
                child_amount = amount - total_distributed
            else:
                child_amount = round(share_per_child)
                total_distributed += child_amount

            if child.person.is_alive:
                child.person.share = child_amount
                self.result.total_distributed += child_amount
            else:
                self._distribute_to_children(child.children, child_amount)

    def _distribute_second_degree(self, root: FamilyNode):
        """Distribute inheritance to second degree heirs (spouse, parents, siblings)"""
        spouse_share = 0.5 if root.spouse and root.spouse.is_alive else 0

        if spouse_share > 0:
            root.spouse.share = round(self.total_value * spouse_share)
            self.result.total_distributed += root.spouse.share

        remaining_amount = self.total_value - self.result.total_distributed
        maternal_amount = remaining_amount / 2
        paternal_amount = remaining_amount - round(maternal_amount, 2)

        # Distribute maternal side
        if root.parents.get(ParentType.MOTHER):
            self._distribute_parent_share(
                root.parents[ParentType.MOTHER],
                root.person.id,
                round(maternal_amount, 2)
            )

        # Distribute paternal side
        if root.parents.get(ParentType.FATHER):
            self._distribute_parent_share(
                root.parents[ParentType.FATHER],
                root.person.id,
                paternal_amount
            )

    def _distribute_parent_share(self, parent_node: FamilyNode, deceased_id: str, amount: float):
        """Distribute a parent's share to them or their descendants"""
        if parent_node.person and parent_node.person.is_alive:
            parent_node.person.share = amount
            self.result.total_distributed += amount
            return

        # Get valid siblings (excluding deceased)
        valid_siblings = []
        for child in parent_node.children:
            if child.person.id != deceased_id:
                if child.person.is_alive:
                    valid_siblings.append(child)
                elif self._has_living_descendants(child):
                    valid_siblings.append(child)

        if not valid_siblings:
            return

        share_per_sibling = amount / len(valid_siblings)
        total_distributed = 0

        for i, sibling in enumerate(valid_siblings):
            # Last sibling gets the remainder to ensure total is exact
            if i == len(valid_siblings) - 1:
                sibling_amount = amount - total_distributed
            else:
                sibling_amount = round(share_per_sibling, 2)
                total_distributed += sibling_amount

            if sibling.person.is_alive:
                sibling.person.share = sibling_amount
                self.result.total_distributed += sibling_amount
            else:
                self._distribute_to_children(sibling.children, sibling_amount)

    def _distribute_third_degree(self, root: FamilyNode):
        """Distribute inheritance to third degree heirs (spouse, grandparents, uncles/aunts)"""
        spouse_share = 0.75 if root.spouse and root.spouse.is_alive else 0

        if spouse_share > 0:
            root.spouse.share = round(self.total_value * spouse_share)
            self.result.total_distributed += root.spouse.share

        remaining_amount = self.total_value - self.result.total_distributed

        # Count living sides
        maternal_side = root.parents and root.parents.get(ParentType.MOTHER)
        paternal_side = root.parents and root.parents.get(ParentType.FATHER)

        if maternal_side and paternal_side:
            # Both sides exist, split remaining amount
            maternal_amount = remaining_amount / 2
            paternal_amount = remaining_amount - round(maternal_amount)

            # Distribute maternal side
            self._distribute_grandparents_share(root.parents[ParentType.MOTHER], round(maternal_amount))

            # Distribute paternal side
            self._distribute_grandparents_share(root.parents[ParentType.FATHER], paternal_amount)
        elif maternal_side:
            # Only maternal side exists, give all remaining amount
            self._distribute_grandparents_share(root.parents[ParentType.MOTHER], remaining_amount)
        elif paternal_side:
            # Only paternal side exists, give all remaining amount
            self._distribute_grandparents_share(root.parents[ParentType.FATHER], remaining_amount)

    def _distribute_grandparents_share(self, parent_node: FamilyNode, amount: float):
        """Distribute a side's share among grandparents or their children (uncles/aunts)"""
        if not parent_node.parents:
            return

        grandmother = parent_node.parents.get(ParentType.MOTHER)
        grandfather = parent_node.parents.get(ParentType.FATHER)

        # Count living grandparents
        living_grandparents = []
        if grandmother and grandmother.person and grandmother.person.is_alive:
            living_grandparents.append(grandmother)
        if grandfather and grandfather.person and grandfather.person.is_alive:
            living_grandparents.append(grandfather)

        # Count living uncles/aunts
        living_uncles = []
        for grandparent in [grandmother, grandfather]:
            if grandparent:
                for uncle in grandparent.children:
                    if (uncle.person and uncle.person.is_alive and 
                        uncle.person.id != parent_node.person.id):
                        living_uncles.append(uncle)

        if living_grandparents and living_uncles:
            # Split amount between grandparents and uncles/aunts
            grandparent_share = amount / 2
            uncle_share = amount - round(grandparent_share)

            # Distribute grandparent share
            share_per_grandparent = grandparent_share / len(living_grandparents)
            total_distributed = 0

            for i, grandparent in enumerate(living_grandparents):
                if i == len(living_grandparents) - 1:
                    share = round(grandparent_share) - total_distributed
                else:
                    share = round(share_per_grandparent)
                    total_distributed += share

                grandparent.person.share = share
                self.result.total_distributed += share

            # Distribute uncle share
            share_per_uncle = uncle_share / len(living_uncles)
            total_distributed = 0

            for i, uncle in enumerate(living_uncles):
                if i == len(living_uncles) - 1:
                    share = uncle_share - total_distributed
                else:
                    share = round(share_per_uncle)
                    total_distributed += share

                uncle.person.share = share
                self.result.total_distributed += share

        elif living_grandparents:
            # Only living grandparents get the share
            share_per_grandparent = amount / len(living_grandparents)
            total_distributed = 0

            for i, grandparent in enumerate(living_grandparents):
                if i == len(living_grandparents) - 1:
                    share = amount - total_distributed
                else:
                    share = round(share_per_grandparent)
                    total_distributed += share

                grandparent.person.share = share
                self.result.total_distributed += share

        elif living_uncles:
            # Only living uncles/aunts get the share
            share_per_uncle = amount / len(living_uncles)
            total_distributed = 0

            for i, uncle in enumerate(living_uncles):
                if i == len(living_uncles) - 1:
                    share = amount - total_distributed
                else:
                    share = round(share_per_uncle)
                    total_distributed += share

                uncle.person.share = share
                self.result.total_distributed += share 