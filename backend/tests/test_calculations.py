import pytest
from app.models import Estate, FamilyTree, Heir, RelationType, FamilyBranch, ParentType
from app.calculations import calculate_inheritance_shares

def test_spouse_only():
    """Test case: Only spouse inherits
    
    Family structure:
    - Spouse (living)
    
    Expected shares:
    - Spouse: 1,000,000 (100% of estate)
    """
    family_tree = FamilyTree()
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    family_tree.add_heir(spouse)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    assert result.family_tree.spouse.share == 1000000

def test_spouse_with_children():
    """Test case: Spouse and children inherit
    
    Family structure:
    - Spouse (living)
    - Child1 (living)
    - Child2 (living)
    
    Expected shares:
    - Spouse: 250,000 (1/4 of estate)
    - Child1: 375,000 (3/8 of estate)
    - Child2: 375,000 (3/8 of estate)
    """
    family_tree = FamilyTree()
    
    # Add spouse and children
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    child2 = Heir(id="c2", name="Child2", relation=RelationType.CHILD)
    
    family_tree.add_heir(spouse)
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    assert result.family_tree.spouse.share == 250000  # 1/4
    assert result.family_tree.children[0].share == 375000  # 3/8
    assert result.family_tree.children[1].share == 375000  # 3/8

def test_children_with_deceased_parent():
    """Test case: Children inherit through deceased parent
    
    Family structure:
    - Child1 (living)
    - Child2 (deceased)
        - Child2's Child1 (living)
        - Child2's Child2 (living)
    
    Expected shares:
    - Child1: 500,000 (1/2 of estate)
    - Child2's branch: 500,000 (1/2 of estate)
        - Child2's Child1: 250,000 (1/4 of estate)
        - Child2's Child2: 250,000 (1/4 of estate)
    """
    family_tree = FamilyTree()
    
    # Add children
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    child2 = Heir(
        id="c2",
        name="Child2",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD),
            Heir(id="c2c2", name="Child2's Child2", relation=RelationType.CHILD)
        ]
    )
    
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    assert result.family_tree.children[0].share == 500000  # 1/2
    child2_children = result.family_tree.children[1].children
    assert child2_children[0].share == 250000  # 1/4
    assert child2_children[1].share == 250000  # 1/4

def test_complex_family_tree():
    """Test case: Complex family tree with multiple generations
    
    Family structure:
    - Spouse (living)
    - Child1 (living)
    - Child2 (deceased)
        - Child2's Child1 (living)
        - Child2's Child2 (deceased)
            - Child2's Child2's Child1 (living)
            - Child2's Child2's Child2 (living)
            - Child2's Child2's Child3 (living)
    
    Expected shares:
    - Spouse: 250,000 (1/4 of estate)
    - Child1: 375,000 (3/8 of estate)
    - Child2's branch: 375,000 (3/8 of estate)
        - Child2's Child1: 187,500 (1/2 of Child2's share)
        - Child2's Child2's children: 187,500 (1/2 of Child2's share)
            - Child2's Child2's Child1: 62,500 (1/3 of Child2's Child2's share)
            - Child2's Child2's Child2: 62,500 (1/3 of Child2's Child2's share)
            - Child2's Child2's Child3: 62,500 (1/3 of Child2's Child2's share)
    """
    family_tree = FamilyTree()
    
    # Add spouse
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    
    # Add children
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    child2 = Heir(
        id="c2",
        name="Child2",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD),
            Heir(
                id="c2c2",
                name="Child2's Child2",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c2c2c1", name="Child2's Child2's Child1", relation=RelationType.CHILD),
                    Heir(id="c2c2c2", name="Child2's Child2's Child2", relation=RelationType.CHILD),
                    Heir(id="c2c2c3", name="Child2's Child2's Child3", relation=RelationType.CHILD)
                ]
            )
        ]
    )
    
    family_tree.add_heir(spouse)
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify shares
    assert result.family_tree.spouse.share == pytest.approx(250000)  # 1/4
    assert result.family_tree.children[0].share == pytest.approx(375000)  # 3/8
    
    # Verify deceased child's branch (3/8 = 375000)
    deceased_child = result.family_tree.children[1]
    assert deceased_child.children[0].share == pytest.approx(187500)  # 1/2 of branch
    
    for ggc in deceased_child.children[1].children:
        assert pytest.approx(ggc.share, rel=1e-4) == 62500  # 1/6 of branch

def test_grandparents_inheritance():
    """Test case: Inheritance through grandparents
    
    Family structure:
    Maternal side (1/2 of estate = 500,000):
    - MaternalGP1 (deceased)
        - MaternalGP1's Child1 (living)
        - MaternalGP1's Child2 (living)
    - MaternalGP2 (living)
    
    Paternal side (1/2 of estate = 500,000):
    - PaternalGP1 (living)
    - PaternalGP2 (deceased)
        - PaternalGP2's Child1 (living)
        - PaternalGP2's Child2 (living)
        - PaternalGP2's Child3 (living)
    
    Expected shares:
    Maternal side:
    - MaternalGP2: 250,000 (1/4 of estate)
    - MaternalGP1's Child1: 125,000 (1/8 of estate)
    - MaternalGP1's Child2: 125,000 (1/8 of estate)
    
    Paternal side:
    - PaternalGP1: 250,000 (1/4 of estate)
    - PaternalGP2's Child1: 83,333.33 (1/12 of estate)
    - PaternalGP2's Child2: 83,333.33 (1/12 of estate)
    - PaternalGP2's Child3: 83,333.33 (1/12 of estate)
    """
    family_tree = FamilyTree()
    
    # Add maternal grandparents
    maternal_gp2 = Heir(
        id="mgp2",
        name="MaternalGP2",
        relation=RelationType.GRANDPARENT,
        branch=FamilyBranch.MATERNAL
    )
    maternal_gp1 = Heir(
        id="mgp1",
        name="MaternalGP1",
        relation=RelationType.GRANDPARENT,
        branch=FamilyBranch.MATERNAL,
        is_alive=False,
        children=[
            Heir(id="ma1", name="MaternalGP1's Child1", relation=RelationType.CHILD),
            Heir(id="ma2", name="MaternalGP1's Child2", relation=RelationType.CHILD)
        ]
    )
    
    # Add paternal grandparents
    paternal_gp1 = Heir(
        id="pgp1",
        name="PaternalGP1",
        relation=RelationType.GRANDPARENT,
        branch=FamilyBranch.PATERNAL
    )
    paternal_gp2 = Heir(
        id="pgp2",
        name="PaternalGP2",
        relation=RelationType.GRANDPARENT,
        branch=FamilyBranch.PATERNAL,
        is_alive=False,
        children=[
            Heir(id="pa1", name="PaternalGP2's Child1", relation=RelationType.CHILD),
            Heir(id="pa2", name="PaternalGP2's Child2", relation=RelationType.CHILD),
            Heir(id="pa3", name="PaternalGP2's Child3", relation=RelationType.CHILD)
        ]
    )
    
    # Add heirs in the correct order
    family_tree.add_heir(maternal_gp2)  # Living maternal GP first
    family_tree.add_heir(maternal_gp1)  # Deceased maternal GP second
    family_tree.add_heir(paternal_gp1)  # Living paternal GP first
    family_tree.add_heir(paternal_gp2)  # Deceased paternal GP second
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify maternal side (1/2 = 500000)
    assert result.family_tree.maternal_grandparents[0].share == 250000  # Living GP gets 1/4
    maternal_aunts = result.family_tree.maternal_grandparents[1].children
    assert maternal_aunts[0].share == 125000  # 1/8
    assert maternal_aunts[1].share == 125000  # 1/8
    
    # Verify paternal side (1/2 = 500000)
    assert result.family_tree.paternal_grandparents[0].share == 250000  # Living GP gets 1/4
    paternal_aunts = result.family_tree.paternal_grandparents[1].children
    assert pytest.approx(paternal_aunts[0].share, rel=1e-4) == 83333.33  # 1/12
    assert pytest.approx(paternal_aunts[1].share, rel=1e-4) == 83333.33  # 1/12
    assert pytest.approx(paternal_aunts[2].share, rel=1e-4) == 83333.33  # 1/12

def test_supercomplex_family_tree():
    """Test case: Super complex family tree with multiple generations and branches
    
    Family structure:
    - Spouse (living)
    - Child1 (living)
    - Child2 (deceased)
        - Child2's Child1 (living)
        - Child2's Child2 (deceased)
            - Child2's Child2's Child1 (living)
            - Child2's Child2's Child2 (living)
            - Child2's Child2's Child3 (living)
    - Child3 (deceased)
        - Child3's Child1 (living)
        - Child3's Child2 (living)
        - Child3's Child3 (deceased)
            - Child3's Child3's Child1 (living)
            - Child3's Child3's Child2 (living)
    
    Expected shares:
    - Spouse: 250,000 (1/4 of estate)
    - Child1: 250,000 (1/3 of remaining 750,000)
    - Child2's branch: 250,000 (1/3 of remaining 750,000)
        - Child2's Child1: 125,000 (1/2 of Child2's share)
        - Child2's Child2's children: 125,000 (1/2 of Child2's share)
            - Child2's Child2's Child1: 41,666.67 (1/3 of Child2's Child2's share)
            - Child2's Child2's Child2: 41,666.67 (1/3 of Child2's Child2's share)
            - Child2's Child2's Child3: 41,666.67 (1/3 of Child2's Child2's share)
    - Child3's branch: 250,000 (1/3 of remaining 750,000)
        - Child3's Child1: 83,333.33 (1/3 of Child3's share)
        - Child3's Child2: 83,333.33 (1/3 of Child3's share)
        - Child3's Child3's children: 83,333.33 (1/3 of Child3's share)
            - Child3's Child3's Child1: 41,666.67 (1/2 of Child3's Child3's share)
            - Child3's Child3's Child2: 41,666.67 (1/2 of Child3's Child3's share)
    """
    family_tree = FamilyTree()
    
    # Add spouse
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    
    # Add first child (living)
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    
    # Add second child (deceased) with complex descendants
    child2 = Heir(
        id="c2",
        name="Child2",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD),
            Heir(
                id="c2c2",
                name="Child2's Child2",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c2c2c1", name="Child2's Child2's Child1", relation=RelationType.CHILD),
                    Heir(id="c2c2c2", name="Child2's Child2's Child2", relation=RelationType.CHILD),
                    Heir(id="c2c2c3", name="Child2's Child2's Child3", relation=RelationType.CHILD)
                ]
            )
        ]
    )
    
    # Add third child (deceased) with complex descendants
    child3 = Heir(
        id="c3",
        name="Child3",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c3c1", name="Child3's Child1", relation=RelationType.CHILD),
            Heir(id="c3c2", name="Child3's Child2", relation=RelationType.CHILD),
            Heir(
                id="c3c3",
                name="Child3's Child3",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c3c3c1", name="Child3's Child3's Child1", relation=RelationType.CHILD),
                    Heir(id="c3c3c2", name="Child3's Child3's Child2", relation=RelationType.CHILD)
                ]
            )
        ]
    )
    
    family_tree.add_heir(spouse)
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    family_tree.add_heir(child3)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify shares
    assert result.family_tree.spouse.share == pytest.approx(250000)  # 1/4
    assert result.family_tree.children[0].share == pytest.approx(250000)  # 1/3 of remaining
    
    # Verify second child's branch (1/3 of remaining = 250000)
    child2_branch = result.family_tree.children[1]
    assert child2_branch.children[0].share == pytest.approx(125000)  # 1/2 of branch
    for c2c2c in child2_branch.children[1].children:
        assert c2c2c.share == pytest.approx(41666.67, rel=1e-4)  # 1/6 of branch
    
    # Verify third child's branch (1/3 of remaining = 250000)
    child3_branch = result.family_tree.children[2]
    assert child3_branch.children[0].share == pytest.approx(83333.33, rel=1e-4)  # 1/3 of branch
    assert child3_branch.children[1].share == pytest.approx(83333.33, rel=1e-4)  # 1/3 of branch
    for c3c3c in child3_branch.children[2].children:
        assert c3c3c.share == pytest.approx(41666.67, rel=1e-4)  # 1/6 of branch

def test_all_deceased_with_descendants():
    """Test case: All primary heirs are deceased but have living descendants
    
    Family structure:
    - Spouse (deceased)
        - Spouse's Child1 (living)
        - Spouse's Child2 (living)
    - Child1 (deceased)
        - Child1's Child1 (living)
        - Child1's Child2 (living)
        - Child1's Child3 (living)
    - Child2 (deceased)
        - Child2's Child1 (living)
        - Child2's Child2 (living)
    - Child3 (deceased)
        - Child3's Child1 (living)
        - Child3's Child2 (living)
        - Child3's Child3 (living)
        - Child3's Child4 (living)
    
    Expected shares:
    Spouse's branch (1/4 = 250,000):
    - Spouse's Child1: 125,000 (1/2 of spouse's share)
    - Spouse's Child2: 125,000 (1/2 of spouse's share)
    
    Children's branches (3/4 = 750,000):
    Child1's branch (1/3 of 750,000 = 250,000):
    - Child1's Child1: 83,333.33 (1/3 of branch)
    - Child1's Child2: 83,333.33 (1/3 of branch)
    - Child1's Child3: 83,333.33 (1/3 of branch)
    
    Child2's branch (1/3 of 750,000 = 250,000):
    - Child2's Child1: 125,000 (1/2 of branch)
    - Child2's Child2: 125,000 (1/2 of branch)
    
    Child3's branch (1/3 of 750,000 = 250,000):
    - Child3's Child1: 62,500 (1/4 of branch)
    - Child3's Child2: 62,500 (1/4 of branch)
    - Child3's Child3: 62,500 (1/4 of branch)
    - Child3's Child4: 62,500 (1/4 of branch)
    """
    family_tree = FamilyTree()
    
    # Add deceased spouse with living children
    spouse = Heir(
        id="s1",
        name="Spouse",
        relation=RelationType.SPOUSE,
        is_alive=False,
        children=[
            Heir(id="sc1", name="Spouse's Child1", relation=RelationType.CHILD),
            Heir(id="sc2", name="Spouse's Child2", relation=RelationType.CHILD)
        ]
    )
    
    # Add three deceased children with descendants
    child1 = Heir(
        id="c1",
        name="Child1",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c1c1", name="Child1's Child1", relation=RelationType.CHILD),
            Heir(id="c1c2", name="Child1's Child2", relation=RelationType.CHILD),
            Heir(id="c1c3", name="Child1's Child3", relation=RelationType.CHILD)
        ]
    )
    
    child2 = Heir(
        id="c2",
        name="Child2",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD),
            Heir(id="c2c2", name="Child2's Child2", relation=RelationType.CHILD)
        ]
    )
    
    child3 = Heir(
        id="c3",
        name="Child3",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c3c1", name="Child3's Child1", relation=RelationType.CHILD),
            Heir(id="c3c2", name="Child3's Child2", relation=RelationType.CHILD),
            Heir(id="c3c3", name="Child3's Child3", relation=RelationType.CHILD),
            Heir(id="c3c4", name="Child3's Child4", relation=RelationType.CHILD)
        ]
    )
    
    family_tree.add_heir(spouse)
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    family_tree.add_heir(child3)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify spouse's branch (1/4 = 250000)
    spouse_children = result.family_tree.spouse.children
    assert spouse_children[0].share == 125000  # 1/2 of spouse's share
    assert spouse_children[1].share == 125000  # 1/2 of spouse's share
    
    # Verify children's branches (3/4 = 750000)
    # First child's branch (1/3 of 750000 = 250000)
    child1_children = result.family_tree.children[0].children
    for c1c in child1_children:
        assert pytest.approx(c1c.share, rel=1e-4) == 83333.33  # 1/3 of branch
    
    # Second child's branch (1/3 of 750000 = 250000)
    child2_children = result.family_tree.children[1].children
    assert child2_children[0].share == 125000  # 1/2 of branch
    assert child2_children[1].share == 125000  # 1/2 of branch
    
    # Third child's branch (1/3 of 750000 = 250000)
    child3_children = result.family_tree.children[2].children
    for c3c in child3_children:
        assert pytest.approx(c3c.share, rel=1e-4) == 62500  # 1/4 of branch 

def test_first_degree_simple():
    """Test case: Simple first-degree inheritance (only children)
    
    Family structure:
    - Child1 (living)
    - Child2 (living)
    - Child3 (living)
    
    Expected shares:
    - Child1: 333,333.33 (1/3 of estate)
    - Child2: 333,333.33 (1/3 of estate)
    - Child3: 333,333.33 (1/3 of estate)
    """
    family_tree = FamilyTree()
    
    # Add three living children
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    child2 = Heir(id="c2", name="Child2", relation=RelationType.CHILD)
    child3 = Heir(id="c3", name="Child3", relation=RelationType.CHILD)
    
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    family_tree.add_heir(child3)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify equal distribution among children
    for child in result.family_tree.children:
        assert pytest.approx(child.share, rel=1e-4) == 333333.33  # 1/3 each

def test_first_degree_mixed():
    """Test case: Mixed first-degree inheritance (spouse and one child)
    
    Family structure:
    - Spouse (living)
    - Child1 (living)
    
    Expected shares:
    - Spouse: 250,000 (1/4 of estate)
    - Child1: 750,000 (3/4 of estate)
    """
    family_tree = FamilyTree()
    
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    child = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    
    family_tree.add_heir(spouse)
    family_tree.add_heir(child)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    assert result.family_tree.spouse.share == 250000  # 1/4
    assert result.family_tree.children[0].share == 750000  # 3/4

def test_second_degree_simple():
    """Test case: Simple second-degree inheritance (only children of deceased children)
    
    Family structure:
    - Child1 (deceased)
        - Child1's Child1 (living)
        - Child1's Child2 (living)
    - Child2 (deceased)
        - Child2's Child1 (living)
    
    Expected shares:
    Child1's branch (1/2 of estate = 500,000):
    - Child1's Child1: 250,000 (1/4 of estate)
    - Child1's Child2: 250,000 (1/4 of estate)
    
    Child2's branch (1/2 of estate = 500,000):
    - Child2's Child1: 500,000 (1/2 of estate)
    """
    family_tree = FamilyTree()
    
    child1 = Heir(
        id="c1",
        name="Child1",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c1c1", name="Child1's Child1", relation=RelationType.CHILD),
            Heir(id="c1c2", name="Child1's Child2", relation=RelationType.CHILD)
        ]
    )
    
    child2 = Heir(
        id="c2",
        name="Child2",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD)
        ]
    )
    
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify first child's branch
    child1_children = result.family_tree.children[0].children
    assert child1_children[0].share == 250000  # 1/4
    assert child1_children[1].share == 250000  # 1/4
    
    # Verify second child's branch
    child2_children = result.family_tree.children[1].children
    assert child2_children[0].share == 500000  # 1/2

def test_second_degree_mixed():
    """Test case: Mixed second-degree inheritance (living and deceased children)
    
    Family structure:
    - Child1 (living)
    - Child2 (deceased)
        - Child2's Child1 (living)
        - Child2's Child2 (living)
    - Child3 (deceased)
        - Child3's Child1 (living)
        - Child3's Child2 (deceased)
            - Child3's Child2's Child1 (living)
    
    Expected shares:
    - Child1: 333,333.33 (1/3 of estate)
    
    Child2's branch (1/3 of estate = 333,333.33):
    - Child2's Child1: 166,666.67 (1/6 of estate)
    - Child2's Child2: 166,666.67 (1/6 of estate)
    
    Child3's branch (1/3 of estate = 333,333.33):
    - Child3's Child1: 166,666.67 (1/6 of estate)
    - Child3's Child2's child: 166,666.67 (1/6 of estate)
        - Child3's Child2's Child1: 166,666.67
    """
    family_tree = FamilyTree()
    
    # Add living child
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    
    # Add deceased child with living children
    child2 = Heir(
        id="c2",
        name="Child2",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD),
            Heir(id="c2c2", name="Child2's Child2", relation=RelationType.CHILD)
        ]
    )
    
    # Add deceased child with mixed descendants
    child3 = Heir(
        id="c3",
        name="Child3",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c3c1", name="Child3's Child1", relation=RelationType.CHILD),
            Heir(
                id="c3c2",
                name="Child3's Child2",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c3c2c1", name="Child3's Child2's Child1", relation=RelationType.CHILD)
                ]
            )
        ]
    )
    
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    family_tree.add_heir(child3)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify living child's share
    assert pytest.approx(result.family_tree.children[0].share, rel=1e-4) == 333333.33  # 1/3
    
    # Verify second child's branch
    child2_children = result.family_tree.children[1].children
    for c2c in child2_children:
        assert pytest.approx(c2c.share, rel=1e-4) == 166666.67  # 1/6
    
    # Verify third child's branch
    child3_branch = result.family_tree.children[2]
    assert pytest.approx(child3_branch.children[0].share, rel=1e-4) == 166666.67  # 1/6
    assert pytest.approx(child3_branch.children[1].children[0].share, rel=1e-4) == 166666.67  # 1/6

def test_third_degree_simple():
    """Test case: Simple third-degree inheritance (only children of deceased children's children)
    
    Family structure:
    - Child1 (deceased)
        - Child1's Child1 (deceased)
            - Child1's Child1's Child1 (living)
            - Child1's Child1's Child2 (living)
        - Child1's Child2 (deceased)
            - Child1's Child2's Child1 (living)
    
    Expected shares:
    Child1's Child1's branch (1/2 of estate = 500,000):
    - Child1's Child1's Child1: 250,000 (1/4 of estate)
    - Child1's Child1's Child2: 250,000 (1/4 of estate)
    
    Child1's Child2's branch (1/2 of estate = 500,000):
    - Child1's Child2's Child1: 500,000 (1/2 of estate)
    """
    family_tree = FamilyTree()
    
    # Create a three-generation family with all ancestors deceased
    child = Heir(
        id="c1",
        name="Child1",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(
                id="c1c1",
                name="Child1's Child1",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c1c1c1", name="Child1's Child1's Child1", relation=RelationType.CHILD),
                    Heir(id="c1c1c2", name="Child1's Child1's Child2", relation=RelationType.CHILD)
                ]
            ),
            Heir(
                id="c1c2",
                name="Child1's Child2",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c1c2c1", name="Child1's Child2's Child1", relation=RelationType.CHILD)
                ]
            )
        ]
    )
    
    family_tree.add_heir(child)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify first child's branch (1/2 = 500000)
    child1_child1_children = result.family_tree.children[0].children[0].children
    assert pytest.approx(child1_child1_children[0].share, rel=1e-4) == 250000  # 1/4
    assert pytest.approx(child1_child1_children[1].share, rel=1e-4) == 250000  # 1/4
    
    # Verify second child's branch (1/2 = 500000)
    child1_child2_children = result.family_tree.children[0].children[1].children
    assert pytest.approx(child1_child2_children[0].share, rel=1e-4) == 500000  # 1/2

def test_mixed_degrees_complex():
    """Test case: Complex mixed-degree inheritance
    
    Family structure:
    - Spouse (living)
    - Child1 (living)
    - Child2 (deceased)
        - Child2's Child1 (living)
        - Child2's Child2 (deceased)
            - Child2's Child2's Child1 (living)
            - Child2's Child2's Child2 (deceased)
                - Child2's Child2's Child2's Child1 (living)
    - Child3 (deceased)
        - Child3's Child1 (deceased)
            - Child3's Child1's Child1 (living)
            - Child3's Child1's Child2 (living)
        - Child3's Child2 (living)
    
    Expected shares:
    - Spouse: 250,000 (1/4 of estate)
    
    Remaining 750,000 split among children's branches:
    - Child1: 250,000 (1/3 of remaining)
    
    Child2's branch (1/3 of remaining = 250,000):
    - Child2's Child1: 125,000 (1/2 of branch)
    - Child2's Child2's descendants: 125,000 (1/2 of branch)
        - Child2's Child2's Child1: 62,500 (1/4 of branch)
        - Child2's Child2's Child2's child: 62,500 (1/4 of branch)
            - Child2's Child2's Child2's Child1: 62,500
    
    Child3's branch (1/3 of remaining = 250,000):
    - Child3's Child1's children: 125,000 (1/2 of branch)
        - Child3's Child1's Child1: 62,500 (1/4 of branch)
        - Child3's Child1's Child2: 62,500 (1/4 of branch)
    - Child3's Child2: 125,000 (1/2 of branch)
    """
    family_tree = FamilyTree()
    
    # Add spouse and living child
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    child1 = Heir(id="c1", name="Child1", relation=RelationType.CHILD)
    
    # Add deceased child with complex descendants
    child2 = Heir(
        id="c2",
        name="Child2",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(id="c2c1", name="Child2's Child1", relation=RelationType.CHILD),
            Heir(
                id="c2c2",
                name="Child2's Child2",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c2c2c1", name="Child2's Child2's Child1", relation=RelationType.CHILD),
                    Heir(
                        id="c2c2c2",
                        name="Child2's Child2's Child2",
                        relation=RelationType.CHILD,
                        is_alive=False,
                        children=[
                            Heir(id="c2c2c2c1", name="Child2's Child2's Child2's Child1", relation=RelationType.CHILD)
                        ]
                    )
                ]
            )
        ]
    )
    
    # Add deceased child with mixed descendants
    child3 = Heir(
        id="c3",
        name="Child3",
        relation=RelationType.CHILD,
        is_alive=False,
        children=[
            Heir(
                id="c3c1",
                name="Child3's Child1",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(id="c3c1c1", name="Child3's Child1's Child1", relation=RelationType.CHILD),
                    Heir(id="c3c1c2", name="Child3's Child1's Child2", relation=RelationType.CHILD)
                ]
            ),
            Heir(id="c3c2", name="Child3's Child2", relation=RelationType.CHILD)
        ]
    )
    
    family_tree.add_heir(spouse)
    family_tree.add_heir(child1)
    family_tree.add_heir(child2)
    family_tree.add_heir(child3)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify spouse and living child
    assert result.family_tree.spouse.share == 250000  # 1/4
    assert result.family_tree.children[0].share == 250000  # 1/3 of remaining
    
    # Verify second child's branch
    child2_branch = result.family_tree.children[1]
    assert child2_branch.children[0].share == 125000  # 1/2 of branch
    assert child2_branch.children[1].children[0].share == 62500  # 1/4 of branch
    assert child2_branch.children[1].children[1].children[0].share == 62500  # 1/4 of branch
    
    # Verify third child's branch
    child3_branch = result.family_tree.children[2]
    for c3c1c in child3_branch.children[0].children:
        assert pytest.approx(c3c1c.share, rel=1e-4) == 62500  # 1/4 of branch
    assert child3_branch.children[1].share == 125000  # 1/2 of branch 

def test_parents_inheritance():
    """Test case: Inheritance with parents
    
    Family structure:
    - Mother (living)
    - Father (living)
    
    Expected shares:
    - Mother: 500,000 (1/2 of estate)
    - Father: 500,000 (1/2 of estate)
    """
    family_tree = FamilyTree()
    
    # Add parents
    mother = Heir(
        id="m1",
        name="Mother",
        relation=RelationType.PARENT,
        parent_type=ParentType.MOTHER
    )
    father = Heir(
        id="f1",
        name="Father",
        relation=RelationType.PARENT,
        parent_type=ParentType.FATHER
    )
    
    family_tree.add_heir(mother)
    family_tree.add_heir(father)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    assert result.family_tree.mother.share == 500000  # 1/2
    assert result.family_tree.father.share == 500000  # 1/2

def test_parents_with_spouse():
    """Test case: Inheritance with parents and spouse
    
    Family structure:
    - Spouse (living)
    - Mother (living)
    - Father (living)
    
    Expected shares:
    - Spouse: 500,000 (1/2 of estate)
    - Mother: 250,000 (1/4 of estate)
    - Father: 250,000 (1/4 of estate)
    """
    family_tree = FamilyTree()
    
    # Add spouse and parents
    spouse = Heir(id="s1", name="Spouse", relation=RelationType.SPOUSE)
    mother = Heir(
        id="m1",
        name="Mother",
        relation=RelationType.PARENT,
        parent_type=ParentType.MOTHER
    )
    father = Heir(
        id="f1",
        name="Father",
        relation=RelationType.PARENT,
        parent_type=ParentType.FATHER
    )
    
    family_tree.add_heir(spouse)
    family_tree.add_heir(mother)
    family_tree.add_heir(father)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    assert result.family_tree.spouse.share == 500000  # 1/2
    assert result.family_tree.mother.share == 250000  # 1/4
    assert result.family_tree.father.share == 250000  # 1/4

def test_deceased_parents_with_children():
    """Test case: Inheritance with deceased parents who have children
    
    Family structure:
    - Mother (deceased)
        - Mother's Child1 (living)
        - Mother's Child2 (living)
    - Father (deceased)
        - Father's Child1 (living)
    
    Expected shares:
    Mother's branch (1/2 of estate = 500,000):
    - Mother's Child1: 250,000 (1/4 of estate)
    - Mother's Child2: 250,000 (1/4 of estate)
    
    Father's branch (1/2 of estate = 500,000):
    - Father's Child1: 500,000 (1/2 of estate)
    """
    family_tree = FamilyTree()
    
    # Add deceased mother with children
    mother = Heir(
        id="m1",
        name="Mother",
        relation=RelationType.PARENT,
        parent_type=ParentType.MOTHER,
        is_alive=False,
        children=[
            Heir(id="mc1", name="Mother's Child1", relation=RelationType.CHILD),
            Heir(id="mc2", name="Mother's Child2", relation=RelationType.CHILD)
        ]
    )
    
    # Add deceased father with child
    father = Heir(
        id="f1",
        name="Father",
        relation=RelationType.PARENT,
        parent_type=ParentType.FATHER,
        is_alive=False,
        children=[
            Heir(id="fc1", name="Father's Child1", relation=RelationType.CHILD)
        ]
    )
    
    family_tree.add_heir(mother)
    family_tree.add_heir(father)
    
    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)
    
    # Verify mother's branch
    assert result.family_tree.mother.children[0].share == 250000  # 1/4
    assert result.family_tree.mother.children[1].share == 250000  # 1/4
    
    # Verify father's branch
    assert result.family_tree.father.children[0].share == 500000  # 1/2 

def test_family_tree_with_spouse_and_parents():
    """Test inheritance calculation for a family tree with a spouse and parents, where one parent has children."""
    family_tree = FamilyTree()

    # Add spouse
    spouse = Heir(
        id="spouse1",
        name="marin",
        relation=RelationType.SPOUSE,
        is_alive=True
    )
    family_tree.add_heir(spouse)

    # Add mother
    mother = Heir(
        id="mother1",
        name="meryem",
        relation=RelationType.PARENT,
        is_alive=True,
        parent_type=ParentType.MOTHER
    )
    family_tree.add_heir(mother)

    # Add father with children
    father = Heir(
        id="father1",
        name="abdul",
        relation=RelationType.PARENT,
        is_alive=False,
        parent_type=ParentType.FATHER,
        children=[
            Heir(
                id="sibling1",
                name="fehmi",
                relation=RelationType.CHILD,
                is_alive=True
            ),
            Heir(
                id="sibling2",
                name="johnny",
                relation=RelationType.CHILD,
                is_alive=False,
                children=[
                    Heir(
                        id="nephew1",
                        name="john1c",
                        relation=RelationType.CHILD,
                        is_alive=True
                    ),
                    Heir(
                        id="nephew2",
                        name="john2c",
                        relation=RelationType.CHILD,
                        is_alive=True
                    )
                ]
            )
        ]
    )
    family_tree.add_heir(father)

    estate = Estate(total_value=1000000, family_tree=family_tree)
    result = calculate_inheritance_shares(estate)

    # Verify spouse's share
    assert result.family_tree.spouse is not None
    assert result.family_tree.spouse.share == 250000  # 1/4 of the estate

    # Verify mother's share
    assert result.family_tree.mother is not None
    assert result.family_tree.mother.share == 166666.67  # 1/6 of the estate

    # Verify father's branch shares
    assert result.family_tree.father is not None
    assert result.family_tree.father.children is not None
    
    # Verify father's first child (fehmi)
    fehmi = result.family_tree.father.children[0]
    assert fehmi.name == "fehmi"
    assert fehmi.share == 291666.66  # Half of father's remaining share (7/12 ÷ 2)

    # Verify father's second child's children (john1c and john2c)
    johnny = result.family_tree.father.children[1]
    assert johnny.name == "johnny"
    assert johnny.share == 0  # Deceased, share passed to children

    assert len(johnny.children) == 2
    john1c = johnny.children[0]
    john2c = johnny.children[1]

    # Each nephew gets a quarter of father's remaining share (7/12 ÷ 4)
    assert john1c.share == 145833.33
    assert john2c.share == 145833.33

    # Verify total distribution equals estate value
    total_shares = (
        result.family_tree.spouse.share +
        result.family_tree.mother.share +
        fehmi.share +
        john1c.share +
        john2c.share
    )
    assert pytest.approx(total_shares, rel=1e-4) == 1000000.00 