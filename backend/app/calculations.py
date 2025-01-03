from typing import List, Dict
from app.models import Estate, Heir, RelationType


def calculate_inheritance_shares(estate: Estate) -> Estate:
    def allocate_shares(heirs: List[Heir], total_value: float) -> List[Heir]:
        spouse = None
        other_heirs = []
        spouse_share = 0
        remaining_value = total_value

        # Separate spouse and other heirs
        for heir in heirs:
            if heir.relation == RelationType.SPOUSE:
                spouse = heir
            else:
                other_heirs.append(heir)

        # Group heirs by degree
        first_degree = get_first_degree_heirs(other_heirs)
        second_degree = get_second_degree_heirs(other_heirs)
        third_degree = get_third_degree_heirs(other_heirs)

        # Calculate spouse's share based on the highest degree present
        if first_degree:
            spouse_share = total_value * 0.25  # 1/4
        elif second_degree:
            spouse_share = total_value * 0.5   # 1/2
        elif third_degree:
            spouse_share = total_value * 0.75  # 3/4
        else:
            spouse_share = total_value  # Full estate if no other heirs

        if spouse:
            spouse.share = spouse_share
            remaining_value -= spouse_share

        # Create a list to store all heirs including descendants
        all_heirs = [heir for heir in heirs]
        if spouse:
            all_heirs = [spouse]

        # Distribute remaining inheritance among other heirs
        if first_degree:
            distribute_first_degree(first_degree, remaining_value)
            all_heirs.extend(first_degree)
        elif second_degree:
            distribute_second_degree(second_degree, remaining_value)
            # Add second degree heirs and their descendants
            for parent in second_degree:
                all_heirs.append(parent)
                if parent.children:
                    for child in parent.children:
                        if child not in all_heirs:
                            all_heirs.append(child)
                        if child.children:
                            for grandchild in child.children:
                                if grandchild not in all_heirs:
                                    all_heirs.append(grandchild)
        elif third_degree:
            distribute_third_degree(third_degree, remaining_value)
            all_heirs.extend(third_degree)

        return all_heirs

    def get_first_degree_heirs(heirs: List[Heir]) -> List[Heir]:
        """Get all first degree heirs (children)"""
        return [h for h in heirs if h.relation == RelationType.CHILD]

    def get_second_degree_heirs(heirs: List[Heir]) -> List[Heir]:
        """Get all second degree heirs (parents)"""
        return [h for h in heirs if h.relation == RelationType.PARENT]

    def get_third_degree_heirs(heirs: List[Heir]) -> List[Heir]:
        """Get all third degree heirs (grandparents)"""
        return [h for h in heirs if h.relation == RelationType.GRANDPARENT]

    def distribute_first_degree(heirs: List[Heir], remaining_value: float):
        """Distribute inheritance among first degree heirs (children and their descendants)"""
        # Group heirs by branches (each child represents a branch)
        branches: Dict[str, List[Heir]] = {}
        
        # First, identify all branches (living and deceased children)
        children = [h for h in heirs if h.relation == RelationType.CHILD]
        for child in children:
            if child.is_alive:
                branches[child.name] = [child]
            elif child.children:  # Deceased child with descendants
                # Get living children of deceased child
                living_descendants = [h for h in child.children if h.is_alive]
                if living_descendants:
                    branches[child.name] = living_descendants
        
        # Calculate share per branch
        if branches:
            share_per_branch = remaining_value / len(branches)
            
            # Distribute within each branch
            for branch_heirs in branches.values():
                if branch_heirs:
                    individual_share = share_per_branch / len(branch_heirs)
                    for heir in branch_heirs:
                        heir.share = individual_share

    def distribute_second_degree(heirs: List[Heir], remaining_value: float):
        """Distribute inheritance among second degree heirs (parents and their descendants)"""
        parents = [h for h in heirs if h.relation == RelationType.PARENT]
        share_per_parent = remaining_value / len(parents)
        
        def get_all_living_descendants(heir: Heir) -> List[Heir]:
            """Recursively get all living descendants of an heir"""
            living_descendants = []
            if heir.is_alive:
                living_descendants.append(heir)
            if heir.children:
                for child in heir.children:
                    living_descendants.extend(get_all_living_descendants(child))
            return living_descendants

        # Process each parent's branch
        for parent in parents:
            if parent.is_alive:
                parent.share = share_per_parent
            elif parent.children:
                # First, add all descendants to heirs list
                for child in parent.children:
                    if child not in heirs:
                        heirs.append(child)
                    if child.children:
                        for grandchild in child.children:
                            if grandchild not in heirs:
                                heirs.append(grandchild)

                # Group descendants by branch (each child represents a branch)
                branches: Dict[str, List[Heir]] = {}
                for child in parent.children:
                    if child.is_alive:
                        branches[child.name] = [child]
                    elif child.children:
                        living_descendants = get_all_living_descendants(child)
                        if living_descendants:
                            branches[child.name] = living_descendants

                # Distribute parent's share among branches
                if branches:
                    share_per_branch = share_per_parent / len(branches)
                    for branch_heirs in branches.values():
                        share_per_heir = share_per_branch / len(branch_heirs)
                        for heir in branch_heirs:
                            heir.share = share_per_heir

    def distribute_third_degree(heirs: List[Heir], remaining_value: float):
        """Distribute inheritance among third degree heirs (grandparents)"""
        # Separate maternal and paternal sides
        maternal_side = [h for h in heirs if h.side == "maternal" and h.is_alive]
        paternal_side = [h for h in heirs if h.side == "paternal" and h.is_alive]
        
        # If one side has no living heirs, all remaining value goes to the other side
        if not maternal_side and paternal_side:
            share_per_grandparent = remaining_value / len(paternal_side)
            for grandparent in paternal_side:
                grandparent.share = share_per_grandparent
            return
        elif not paternal_side and maternal_side:
            share_per_grandparent = remaining_value / len(maternal_side)
            for grandparent in maternal_side:
                grandparent.share = share_per_grandparent
            return
        
        # If both sides have living heirs, split between sides
        side_share = remaining_value / 2
        
        # Distribute to maternal side
        if maternal_side:
            share_per_grandparent = side_share / len(maternal_side)
            for grandparent in maternal_side:
                grandparent.share = share_per_grandparent
                
        # Distribute to paternal side
        if paternal_side:
            share_per_grandparent = side_share / len(paternal_side)
            for grandparent in paternal_side:
                grandparent.share = share_per_grandparent

    # Update estate's heirs with the complete list including descendants
    estate.heirs = allocate_shares(estate.heirs, estate.total_value)
    return estate

