import pytest
from app.models import Estate, Heir, RelationType
from app.calculations import calculate_inheritance_shares

def test_spouse_with_children():
    """Test case: Spouse with children"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="Spouse", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="Child1", relation=RelationType.CHILD, is_alive=True),
            Heir(name="Child2", relation=RelationType.CHILD, is_alive=True)
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 250000  # 1/4
    
    children = [h for h in result.heirs if h.relation == RelationType.CHILD]
    for child in children:
        assert child.share == 375000  # (1000000 - 250000) / 2

def test_spouse_with_parents():
    """Test case: Spouse with parents"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="Spouse", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="Parent1", relation=RelationType.PARENT, is_alive=True),
            Heir(name="Parent2", relation=RelationType.PARENT, is_alive=True)
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 500000  # 1/2
    
    parents = [h for h in result.heirs if h.relation == RelationType.PARENT]
    for parent in parents:
        assert parent.share == 250000  # (1000000 - 500000) / 2

def test_spouse_with_grandparents():
    """Test case: Spouse with grandparents"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="Spouse", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="Maternal_Grandmother", relation=RelationType.GRANDPARENT, 
                is_alive=True, side="maternal"),
            Heir(name="Paternal_Grandfather", relation=RelationType.GRANDPARENT, 
                is_alive=True, side="paternal")
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 750000  # 3/4
    
    grandparents = [h for h in result.heirs if h.relation == RelationType.GRANDPARENT]
    for grandparent in grandparents:
        assert grandparent.share == 125000  # (1000000 - 750000) / 2

def test_only_children():
    """Test case: Only children"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="Child1", relation=RelationType.CHILD, is_alive=True),
            Heir(name="Child2", relation=RelationType.CHILD, is_alive=True),
            Heir(name="Child3", relation=RelationType.CHILD, is_alive=True)
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    children = [h for h in result.heirs if h.relation == RelationType.CHILD]
    for child in children:
        assert child.share == 1000000 / 3

def test_only_spouse():
    """Test case: Only spouse"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="Spouse", relation=RelationType.SPOUSE, is_alive=True)
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 1000000

@pytest.mark.parametrize("total_value", [0, 1000000, 777777])
def test_edge_cases(total_value):
    """Test edge cases with different estate values"""
    estate = Estate(
        total_value=total_value,
        heirs=[
            Heir(name="Spouse", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="Child1", relation=RelationType.CHILD, is_alive=True)
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    child = next(h for h in result.heirs if h.relation == RelationType.CHILD)
    
    assert spouse.share == total_value * 0.25
    assert child.share == total_value * 0.75 

def test_spouse_with_two_children():
    """Test case: Spouse with two children
    Example: E=1/4, Children=3/8 each"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="E", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="Child1", relation=RelationType.CHILD, is_alive=True),
            Heir(name="Child2", relation=RelationType.CHILD, is_alive=True)
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 250000  # 1/4
    
    children = [h for h in result.heirs if h.relation == RelationType.CHILD]
    for child in children:
        assert child.share == 375000  # 3/8 each

def test_spouse_with_deceased_child_and_living_child():
    """Test case: Spouse, one deceased child (with two children), one living child
    Example: E=1/4, B=3/8, X=3/16, Y=3/16"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="E", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="B", relation=RelationType.CHILD, is_alive=True),
            Heir(
                name="A", 
                relation=RelationType.CHILD, 
                is_alive=False,
                children=[
                    Heir(name="X", relation=RelationType.CHILD, is_alive=True),
                    Heir(name="Y", relation=RelationType.CHILD, is_alive=True)
                ]
            )
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 250000  # 1/4
    
    living_child = next(h for h in result.heirs if h.name == "B")
    assert living_child.share == 375000  # 3/8
    
    grandchildren = [h for h in result.heirs if h.name in ["X", "Y"]]
    for grandchild in grandchildren:
        assert grandchild.share == 187500  # 3/16 each

def test_spouse_with_both_parents():
    """Test case: Spouse with both parents
    Example: E=1/2, A=1/4, B=1/4"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="E", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="A", relation=RelationType.PARENT, is_alive=True),
            Heir(name="B", relation=RelationType.PARENT, is_alive=True)
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 500000  # 1/2
    
    parents = [h for h in result.heirs if h.relation == RelationType.PARENT]
    for parent in parents:
        assert parent.share == 250000  # 1/4 each

def test_spouse_with_grandparents_complex():
    """Test case: Spouse with maternal and paternal grandparents
    Example: E=3/4, A=1/16, B=1/16, C=1/16, D=1/16"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="E", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="A", relation=RelationType.GRANDPARENT, is_alive=True, side="maternal"),
            Heir(name="B", relation=RelationType.GRANDPARENT, is_alive=True, side="maternal"),
            Heir(name="C", relation=RelationType.GRANDPARENT, is_alive=True, side="paternal"),
            Heir(name="D", relation=RelationType.GRANDPARENT, is_alive=True, side="paternal")
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 750000  # 3/4
    
    grandparents = [h for h in result.heirs if h.relation == RelationType.GRANDPARENT]
    for grandparent in grandparents:
        assert grandparent.share == 62500  # 1/16 each

def test_spouse_with_one_side_grandparents():
    """Test case: Spouse with only maternal grandparents
    Example: E=3/4, A=1/8, D=1/8"""
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="E", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="A", relation=RelationType.GRANDPARENT, is_alive=True, side="maternal"),
            Heir(name="D", relation=RelationType.GRANDPARENT, is_alive=True, side="maternal")
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 750000  # 3/4
    
    grandparents = [h for h in result.heirs if h.relation == RelationType.GRANDPARENT]
    for grandparent in grandparents:
        assert grandparent.share == 125000  # 1/8 each 

def test_second_degree_one_parent_with_complex_descendants():
    """Test case: One living parent, one deceased parent with children and grandchildren
    Example: 
    - Living parent gets 1/4
    - Deceased parent's share (1/4) is split among their descendants:
        * Living sibling gets 1/8
        * Deceased sibling's two children get 1/16 each
    """
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="Spouse", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="LivingParent", relation=RelationType.PARENT, is_alive=True),
            Heir(
                name="DeceasedParent", 
                relation=RelationType.PARENT, 
                is_alive=False,
                children=[
                    Heir(name="LivingSibling", relation=RelationType.CHILD, is_alive=True),
                    Heir(
                        name="DeceasedSibling", 
                        relation=RelationType.CHILD, 
                        is_alive=False,
                        children=[
                            Heir(name="Niece1", relation=RelationType.CHILD, is_alive=True),
                            Heir(name="Niece2", relation=RelationType.CHILD, is_alive=True)
                        ]
                    )
                ]
            )
        ]
    )
    
    result = calculate_inheritance_shares(estate)
    
    # Spouse should get 1/2
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 500000  # 1/2
    
    # Living parent should get 1/4
    living_parent = next(h for h in result.heirs if h.name == "LivingParent")
    assert living_parent.share == 250000  # 1/4
    
    # Living sibling should get 1/8
    living_sibling = next(h for h in result.heirs if h.name == "LivingSibling")
    assert living_sibling.share == 125000  # 1/8
    
    # Each niece should get 1/16
    nieces = [h for h in result.heirs if h.name.startswith("Niece")]
    for niece in nieces:
        assert niece.share == 62500  # 1/16

def test_second_degree_one_parent_multiple_deceased_siblings():
    """Test case: One living parent, one deceased parent with multiple deceased siblings
    Each having different numbers of children
    """
    estate = Estate(
        total_value=1000000,
        heirs=[
            Heir(name="Spouse", relation=RelationType.SPOUSE, is_alive=True),
            Heir(name="LivingParent", relation=RelationType.PARENT, is_alive=True),
            Heir(
                name="DeceasedParent",
                relation=RelationType.PARENT,
                is_alive=False,
                children=[
                    Heir(
                        name="DeceasedSibling1",
                        relation=RelationType.CHILD,
                        is_alive=False,
                        children=[
                            Heir(name="Niece1", relation=RelationType.CHILD, is_alive=True),
                            Heir(name="Niece2", relation=RelationType.CHILD, is_alive=True),
                            Heir(name="Niece3", relation=RelationType.CHILD, is_alive=True)
                        ]
                    ),
                    Heir(
                        name="DeceasedSibling2",
                        relation=RelationType.CHILD,
                        is_alive=False,
                        children=[
                            Heir(name="Nephew1", relation=RelationType.CHILD, is_alive=True)
                        ]
                    )
                ]
            )
        ]
    )

    result = calculate_inheritance_shares(estate)

    # Spouse should get 1/2
    spouse = next(h for h in result.heirs if h.relation == RelationType.SPOUSE)
    assert spouse.share == 500000  # 1/2

    # Living parent should get 1/4
    living_parent = next(h for h in result.heirs if h.name == "LivingParent")
    assert living_parent.share == 250000  # 1/4

    # Deceased parent's share (1/4) should be split between branches
    # First deceased sibling's children (3 nieces) share 1/8
    nieces = [h for h in result.heirs if h.name.startswith("Niece")]
    for niece in nieces:
        assert niece.share == pytest.approx(41666.67, rel=1e-4)  # approximately 1/24

    # Second deceased sibling's child gets 1/8
    nephew = next(h for h in result.heirs if h.name == "Nephew1")
    assert nephew.share == pytest.approx(125000, rel=1e-4)  # 1/8 