from typing import List, Dict
from app.models import Estate, Heir, RelationType, FamilyBranch, FamilyTree
def calculate_inheritance_shares(estate: Estate) -> Estate:
    """Calculate inheritance shares for all heirs in the estate."""
    total_value = estate.total_value
    family_tree = estate.family_tree
    spouse_share = 0

    # Calculate spouse's share
    if family_tree.spouse:
        if family_tree.spouse.is_alive:
            # Check for first degree relatives (children or parents)
            has_first_degree = (
                any(child.is_alive for child in family_tree.children) or
                (family_tree.mother and family_tree.mother.is_alive) or
                (family_tree.father and family_tree.father.is_alive)
            )
            
            # Check for second degree relatives (grandchildren)
            has_second_degree = any(
                grandchild.is_alive 
                for child in family_tree.children if not child.is_alive
                for grandchild in child.children
            )
            
            # Check for third degree relatives (great-grandchildren)
            has_third_degree = any(
                great_grandchild.is_alive
                for child in family_tree.children if not child.is_alive
                for grandchild in child.children if not grandchild.is_alive
                for great_grandchild in grandchild.children
            )

            if has_first_degree:
                spouse_share = total_value * 0.25  # 1/4 if first degree relatives exist
            elif has_second_degree:
                spouse_share = total_value * 0.5   # 1/2 if second degree relatives exist
            elif has_third_degree:
                spouse_share = total_value * 0.75  # 3/4 if third degree relatives exist
            else:
                spouse_share = total_value  # Full estate if no qualifying relatives

            family_tree.spouse.share = round(spouse_share, 2)
        elif family_tree.spouse.children:
            # Handle deceased spouse's children
            spouse_share = total_value * 0.25  # Deceased spouse's share is 1/4
            distribute_to_children(family_tree.spouse.children, spouse_share)

    # If there are children, distribute among them
    if family_tree.children:
        distribute_to_children(family_tree.children, total_value - spouse_share)
    # If no children, check for parents
    elif family_tree.mother or family_tree.father:
        distribute_to_parents(family_tree, total_value, spouse_share)
    # If no parents, distribute among grandparents
    elif family_tree.maternal_grandparents or family_tree.paternal_grandparents:
        distribute_to_grandparents(family_tree, total_value - spouse_share)

    return estate

def distribute_to_children(children: List[Heir], total_value: float) -> None:
    """Distribute inheritance among children and their descendants."""
    # Count valid branches (living children or deceased children with descendants)
    valid_branches = [child for child in children if child.is_alive or (not child.is_alive and child.children)]
    if not valid_branches:
        return

    # Calculate share per branch
    share_per_branch = total_value / len(valid_branches)
    
    # Distribute within each branch
    for child in valid_branches:
        if child.is_alive:
            # Living child gets full branch share
            child.share = round(share_per_branch, 2)
        elif child.children:
            # Handle deceased child's branch
            valid_grandchildren = []
            for grandchild in child.children:
                if grandchild.is_alive:
                    valid_grandchildren.append((grandchild, [grandchild]))
                elif grandchild.children:
                    # If grandchild is deceased, include their branch
                    living_descendants = []
                    for great_grandchild in grandchild.children:
                        if great_grandchild.is_alive:
                            living_descendants.append(great_grandchild)
                        elif great_grandchild.children:
                            # Include living great-great-grandchildren
                            living_descendants.extend([ggc for ggc in great_grandchild.children if ggc.is_alive])
                    if living_descendants:
                        valid_grandchildren.append((grandchild, living_descendants))
            
            if not valid_grandchildren:
                continue
            
            # Calculate share per grandchild's branch
            share_per_grandchild = share_per_branch / len(valid_grandchildren)
            
            # Distribute within each grandchild's branch
            for grandchild, living_descendants in valid_grandchildren:
                if grandchild.is_alive:
                    grandchild.share = round(share_per_grandchild, 2)
                else:
                    # Group descendants by their parent
                    descendant_groups = {}
                    for descendant in living_descendants:
                        parent_id = descendant.id.rsplit('c', 1)[0]
                        if parent_id not in descendant_groups:
                            descendant_groups[parent_id] = []
                        descendant_groups[parent_id].append(descendant)
                    
                    # Calculate share per group
                    share_per_group = share_per_grandchild / len(descendant_groups)
                    
                    # Distribute within each group
                    for group in descendant_groups.values():
                        share_per_descendant = share_per_group / len(group)
                        for descendant in group:
                            descendant.share = round(share_per_descendant, 2)

def distribute_to_parents(family_tree: FamilyTree, total_value: float, spouse_share: float = 0) -> None:
    """Distribute inheritance among parents."""
    living_parents = []
    if family_tree.mother and family_tree.mother.is_alive:
        living_parents.append(family_tree.mother)
    if family_tree.father and family_tree.father.is_alive:
        living_parents.append(family_tree.father)

    remaining_value = total_value - spouse_share

    # If both parents are alive, split equally
    if len(living_parents) == 2:
        share_per_parent = remaining_value / 2
        family_tree.mother.share = round(share_per_parent, 2)
        family_tree.father.share = round(share_per_parent, 2)
    # If one parent is alive
    elif len(living_parents) == 1:
        living_parent = living_parents[0]
        # Living parent gets 1/6 of total estate
        living_parent.share = round(total_value / 6, 2)  # Always 1/6 regardless of spouse

        # Calculate remaining value after spouse and living parent shares
        remaining_value = total_value - spouse_share - living_parent.share

        # Distribute remaining to deceased parent's children if any
        if living_parent == family_tree.mother and family_tree.father and family_tree.father.children:
            distribute_to_children(family_tree.father.children, remaining_value)
        elif living_parent == family_tree.father and family_tree.mother and family_tree.mother.children:
            distribute_to_children(family_tree.mother.children, remaining_value)
    # If both parents are deceased, distribute to their children
    else:
        # Split between maternal and paternal branches
        maternal_value = remaining_value / 2
        paternal_value = remaining_value / 2

        # Distribute mother's share to her children if she has any
        if family_tree.mother and family_tree.mother.children:
            distribute_to_children(family_tree.mother.children, maternal_value)

        # Distribute father's share to his children if he has any
        if family_tree.father and family_tree.father.children:
            distribute_to_children(family_tree.father.children, paternal_value)

def distribute_to_grandparents(family_tree: FamilyTree, total_value: float) -> None:
    """Distribute inheritance among grandparents and their descendants."""
    maternal_value = total_value / 2
    paternal_value = total_value / 2

    # Process maternal side
    if family_tree.maternal_grandparents:
        distribute_to_grandparent_branch(family_tree.maternal_grandparents, maternal_value)

    # Process paternal side
    if family_tree.paternal_grandparents:
        distribute_to_grandparent_branch(family_tree.paternal_grandparents, paternal_value)

def distribute_to_grandparent_branch(grandparents: List[Heir], total_value: float) -> None:
    """Distribute inheritance within a grandparent branch (maternal or paternal)."""
    # Count living grandparents and deceased grandparents with children
    valid_grandparents = [gp for gp in grandparents if gp.is_alive or (not gp.is_alive and gp.children)]
    if not valid_grandparents:
        return
    
    # Calculate share per grandparent
    share_per_grandparent = total_value / len(valid_grandparents)
    
    for grandparent in valid_grandparents:
        if grandparent.is_alive:
            grandparent.share = share_per_grandparent
        elif grandparent.children:
            # Get living descendants grouped by generation
            living_descendants = get_living_descendants_by_generation(grandparent)
            if not living_descendants:
                continue
            
            # Group descendants by generation
            generations = group_by_generation(living_descendants)
            current_share = share_per_grandparent
            current_generation = min(generations.keys())
            
            # Distribute shares within the branch
            while current_generation in generations:
                gen_heirs = generations[current_generation]
                share_per_heir = current_share / len(gen_heirs)
                
                # First pass: distribute to living heirs
                living_heirs = [h for h in gen_heirs if h.is_alive]
                deceased_with_children = [h for h in gen_heirs if not h.is_alive and h.children]
                
                if living_heirs:
                    for heir in living_heirs:
                        heir.share = share_per_heir
                    
                    # If there are deceased heirs with children, their shares pass down
                    if deceased_with_children:
                        remaining_share = share_per_heir * len(deceased_with_children)
                        current_share = remaining_share
                        current_generation += 1
                    else:
                        # If no deceased heirs have children, redistribute their shares
                        deceased_share = share_per_heir * (len(gen_heirs) - len(living_heirs))
                        additional_share = deceased_share / len(living_heirs)
                        for heir in living_heirs:
                            heir.share += additional_share
                        break
                else:
                    # All heirs in this generation are deceased, pass full share to next generation
                    current_generation += 1

def get_living_descendants_by_generation(heir: Heir) -> List[Heir]:
    """Get all living descendants of an heir, maintaining generation information."""
    descendants = []
    
    def collect_descendants(current_heir: Heir, generation: int) -> None:
        if current_heir.children:
            for child in current_heir.children:
                child.generation = generation
                if child.is_alive or child.children:  # Include deceased heirs with children
                    descendants.append(child)
                collect_descendants(child, generation + 1)
    
    collect_descendants(heir, 1)
    return descendants

def group_by_generation(heirs: List[Heir]) -> Dict[int, List[Heir]]:
    """Group heirs by their generation level."""
    generations: Dict[int, List[Heir]] = {}
    for heir in heirs:
        generation = getattr(heir, 'generation', 1)
        if generation not in generations:
            generations[generation] = []
        generations[generation].append(heir)
    return generations

