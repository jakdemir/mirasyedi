import pytest
from app.models import Estate, FamilyTree, Heir, RelationType, FamilyBranch, Person

def test_person_creation():
    person = Person(id="p1", name="John Doe")
    assert person.id == "p1"
    assert person.name == "John Doe"
    assert person.is_alive == True
    assert person.share == 0.0

def test_heir_creation():
    heir = Heir(
        id="h1",
        name="John Doe",
        relation=RelationType.CHILD,
        branch=FamilyBranch.DIRECT
    )
    assert heir.id == "h1"
    assert heir.name == "John Doe"
    assert heir.relation == RelationType.CHILD
    assert heir.branch == FamilyBranch.DIRECT
    assert heir.parent_id is None
    assert heir.children == []

def test_heir_add_child():
    parent = Heir(
        id="p1",
        name="Parent",
        relation=RelationType.CHILD,
        branch=FamilyBranch.DIRECT
    )
    child = Heir(
        id="c1",
        name="Child",
        relation=RelationType.CHILD,
        branch=FamilyBranch.DIRECT
    )
    
    parent.add_child(child)
    assert len(parent.children) == 1
    assert parent.children[0].id == "c1"
    assert parent.children[0].parent_id == "p1"

def test_heir_get_descendants():
    # Create a three-generation family
    grandparent = Heir(
        id="gp1",
        name="Grandparent",
        relation=RelationType.CHILD,
        branch=FamilyBranch.DIRECT
    )
    parent = Heir(
        id="p1",
        name="Parent",
        relation=RelationType.CHILD,
        branch=FamilyBranch.DIRECT
    )
    child = Heir(
        id="c1",
        name="Child",
        relation=RelationType.CHILD,
        branch=FamilyBranch.DIRECT
    )
    
    grandparent.add_child(parent)
    parent.add_child(child)
    
    descendants = grandparent.get_descendants()
    assert len(descendants) == 2
    assert descendants[0].id == "p1"
    assert descendants[1].id == "c1"

def test_family_tree_creation():
    family_tree = FamilyTree()
    assert family_tree.spouse is None
    assert family_tree.children == []
    assert family_tree.maternal_grandparents == []
    assert family_tree.paternal_grandparents == []

def test_family_tree_add_heir():
    family_tree = FamilyTree()
    
    # Add spouse
    spouse = Heir(
        id="s1",
        name="Spouse",
        relation=RelationType.SPOUSE,
        branch=FamilyBranch.DIRECT
    )
    family_tree.add_heir(spouse)
    assert family_tree.spouse == spouse
    
    # Add child
    child = Heir(
        id="c1",
        name="Child",
        relation=RelationType.CHILD,
        branch=FamilyBranch.DIRECT
    )
    family_tree.add_heir(child)
    assert len(family_tree.children) == 1
    assert family_tree.children[0] == child
    
    # Add maternal grandparent
    maternal_gp = Heir(
        id="mgp1",
        name="Maternal Grandparent",
        relation=RelationType.CHILD,
        branch=FamilyBranch.MATERNAL
    )
    family_tree.add_heir(maternal_gp)
    assert len(family_tree.maternal_grandparents) == 1
    assert family_tree.maternal_grandparents[0] == maternal_gp
    
    # Add paternal grandparent
    paternal_gp = Heir(
        id="pgp1",
        name="Paternal Grandparent",
        relation=RelationType.CHILD,
        branch=FamilyBranch.PATERNAL
    )
    family_tree.add_heir(paternal_gp)
    assert len(family_tree.paternal_grandparents) == 1
    assert family_tree.paternal_grandparents[0] == paternal_gp

def test_family_tree_get_methods():
    family_tree = FamilyTree()
    
    # Create heirs
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    child2 = Heir(id="c2", name="Child2", relation=RelationType.CHILD, is_alive=False)
    maternal_gp = Heir(
        id="mgp1",
        name="Maternal GP",
        relation=RelationType.CHILD,
        branch=FamilyBranch.MATERNAL
    )
    paternal_gp = Heir(
        id="pgp1",
        name="Paternal GP",
        relation=RelationType.CHILD,
        branch=FamilyBranch.PATERNAL
    )
    
    # Add heirs to family tree
    family_tree.add_heir(spouse)
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    family_tree.add_heir(maternal_gp)
    family_tree.add_heir(paternal_gp)
    
    # Test get_all_heirs
    all_heirs = family_tree.get_all_heirs()
    assert len(all_heirs) == 5
    assert spouse in all_heirs
    assert child1 in all_heirs
    assert child2 in all_heirs
    assert maternal_gp in all_heirs
    assert paternal_gp in all_heirs
    
    # Test get_living_heirs
    living_heirs = family_tree.get_living_heirs()
    assert len(living_heirs) == 4
    assert child2 not in living_heirs
    
    # Test get_heirs_by_relation
    children = family_tree.get_heirs_by_relation(RelationType.CHILD)
    assert len(children) == 4  # child1, child2, maternal_gp, paternal_gp
    
    # Test get_branch_heirs
    maternal_heirs = family_tree.get_branch_heirs(FamilyBranch.MATERNAL)
    assert len(maternal_heirs) == 1
    assert maternal_gp in maternal_heirs

def test_estate_creation():
    family_tree = FamilyTree()
    estate = Estate(total_value=1000000, family_tree=family_tree)
    assert estate.total_value == 1000000
    assert estate.family_tree == family_tree

def test_complex_family_structure():
    # Create a complex family structure
    family_tree = FamilyTree()
    
    # Add spouse
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    family_tree.add_heir(spouse)
    
    # Add children
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    child2 = Heir(id="c2", name="Child2", relation=RelationType.CHILD, is_alive=False)
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    
    # Add children to deceased child
    child2_child1 = Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD)
    child2_child2 = Heir(id="c2c2", name="Child2's Child2", relation=RelationType.CHILD)
    child2.add_child(child2_child1)
    child2.add_child(child2_child2)
    
    # Verify structure
    assert len(family_tree.get_all_heirs()) == 5
    assert len(child2.children) == 2
    assert child2.children[0].parent_id == "c2"
    assert child2.children[1].parent_id == "c2" 