import pytest
from app.models import (
    Estate, FamilyTree, FamilyNode, Person,
    ParentType, MarriageInfo
)
from app.calculations import InheritanceCalculator

def test_spouse_only():
    """Test case: Only spouse inherits
    
    Family structure:
    - Deceased person
    - Spouse (living)
    
    Expected shares:
    - Spouse: 1,000,000 (100% of estate)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create spouse
    spouse = Person(
        id="s1",
        name="Spouse"
    )

    # Create family tree
    root_node = FamilyNode(
        person=deceased,
        spouse=spouse
    )
    
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    assert result.total_distributed == 1000000
    assert spouse.share == 1000000  # Spouse gets everything

def test_spouse_with_children():
    """Test case: Basic nuclear family
    
    Family structure:
    - Deceased person
    - Spouse (living)
    - Child1 (living)
    - Child2 (living)
    
    Expected shares:
    - Spouse: 250,000 (1/4)
    - Child1: 375,000 (3/8)
    - Child2: 375,000 (3/8)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create spouse
    spouse = Person(
        id="s1",
        name="Spouse"
    )

    # Create children
    child1 = Person(
        id="c1",
        name="Child1",
        parent_id="d1"
    )

    child2 = Person(
        id="c2",
        name="Child2",
        parent_id="d1"
    )

    # Create family tree
    root_node = FamilyNode(
        person=deceased,
        spouse=spouse,
        children=[
            FamilyNode(person=child1),
            FamilyNode(person=child2)
        ]
    )
    
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    assert result.total_distributed == 1000000
    assert spouse.share == 250000   # Spouse: 1/4
    assert child1.share == 375000   # Child1: 3/8
    assert child2.share == 375000   # Child2: 3/8

def test_first_degree_with_half_siblings():
    """Test case: First Degree with Half-Siblings
    
    Family structure:
    - Deceased person
    - Spouse (alive)
    - Child1 (from current marriage, alive)
    - Child2 (from current marriage, deceased)
        - Grandchild1 (alive)
        - Grandchild2 (alive)
    - Child3 (from deceased's previous marriage, alive)
    
    Expected shares:
    - Spouse: 250,000 TL (1/4)
    - Child1: 250,000 TL (1/4)
    - Grandchild1: 125,000 TL (1/8)
    - Grandchild2: 125,000 TL (1/8)
    - Child3: 250,000 TL (1/4)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create spouse
    spouse = Person(
        id="s1",
        name="Spouse",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    # Create children
    child1 = Person(
        id="c1",
        name="Child1",
        parent_id="d1",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    child2 = Person(
        id="c2",
        name="Child2",
        parent_id="d1",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    grandchild1 = Person(
        id="gc1",
        name="Grandchild1",
        parent_id="c2"
    )

    grandchild2 = Person(
        id="gc2",
        name="Grandchild2",
        parent_id="c2"
    )

    child3 = Person(
        id="c3",
        name="Child3",
        parent_id="d1",
        marriage_info=MarriageInfo(marriage_order=1, is_current=False)
    )

    # Create family nodes
    child2_node = FamilyNode(
        person=child2,
        children=[
            FamilyNode(person=grandchild1),
            FamilyNode(person=grandchild2)
        ]
    )

    root_node = FamilyNode(
        person=deceased,
        spouse=spouse,
        children=[
            FamilyNode(person=child1),
            child2_node,
            FamilyNode(person=child3)
        ]
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    assert result.total_distributed == 1000000
    assert spouse.share == 250000  # Spouse: 1/4
    assert child1.share == 250000  # Child1: 1/4
    assert grandchild1.share == 125000  # Grandchild1: 1/8
    assert grandchild2.share == 125000  # Grandchild2: 1/8
    assert child3.share == 250000  # Child3: 1/4

def test_parents_with_spouse():
    """Test case: Both parents alive with spouse
    
    Family structure:
    - Deceased person
    - Spouse (living)
    - Mother (living)
    - Father (living)
    
    Expected shares:
    - Spouse: 500,000 (1/2)
    - Mother: 250,000 (1/4)
    - Father: 250,000 (1/4)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create spouse
    spouse = Person(
        id="s1",
        name="Spouse"
    )

    # Create parents
    mother = Person(
        id="m1",
        name="Mother"
    )

    father = Person(
        id="f1",
        name="Father"
    )

    # Create family tree
    root_node = FamilyNode(
        person=deceased,
        spouse=spouse,
        parents={
            ParentType.MOTHER: FamilyNode(person=mother),
            ParentType.FATHER: FamilyNode(person=father)
        }
    )
    
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    assert result.total_distributed == 1000000
    assert spouse.share == 500000   # Spouse: 1/2
    assert mother.share == 250000   # Mother: 1/4
    assert father.share == 250000   # Father: 1/4

def test_complex_second_degree_with_multiple_marriages():
    """Test case: Complex Second Degree with Multiple Marriages
    
    Family structure:
    - Deceased person (no children)
    - Spouse (alive)
    - Mother (deceased)
        - Full Sibling1 (alive)
        - Full Sibling2 (deceased)
            - Nephew1 (alive)
    - Father (deceased, remarried)
        - Half Sibling1 (from father's second marriage, alive)
        - Half Sibling2 (from father's second marriage, deceased)
            - Half Nephew1 (alive)
    
    Expected shares:
    - Spouse: 500,000 TL (1/2)
    Mother's side 250,000 TL (1/4):
    - Full Sibling1: 125,000 TL (1/8)
    - Nephew1: 125,000 TL (1/8)
    Father's side 250,000 TL (1/4):
    - Half Sibling1: 125,000 TL (1/8)
    - Half Nephew1 125,000 TL (1/8)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create spouse
    spouse = Person(
        id="s1",
        name="Spouse"
    )

    # Create mother's side
    mother = Person(
        id="m1",
        name="Mother",
        is_alive=False
    )

    full_sibling1 = Person(
        id="fs1",
        name="Full Sibling1",
        parent_id="m1"
    )

    full_sibling2 = Person(
        id="fs2",
        name="Full Sibling2",
        parent_id="m1",
        is_alive=False
    )

    nephew1 = Person(
        id="n1",
        name="Nephew1",
        parent_id="fs2"
    )

    # Create father's side
    father = Person(
        id="f1",
        name="Father",
        is_alive=False
    )

    half_sibling1 = Person(
        id="hs1",
        name="Half Sibling1",
        parent_id="f1",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    half_sibling2 = Person(
        id="hs2",
        name="Half Sibling2",
        parent_id="f1",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    half_nephew1 = Person(
        id="hn1",
        name="Half Nephew1",
        parent_id="hs2"
    )

    # Create family nodes
    mother_node = FamilyNode(
        person=mother,
        children=[
            FamilyNode(person=full_sibling1),
            FamilyNode(
                person=full_sibling2,
                children=[FamilyNode(person=nephew1)]
            )
        ]
    )

    father_node = FamilyNode(
        person=father,
        children=[
            FamilyNode(person=half_sibling1),
            FamilyNode(
                person=half_sibling2,
                children=[FamilyNode(person=half_nephew1)]
            )
        ]
    )

    root_node = FamilyNode(
        person=deceased,
        spouse=spouse,
        parents={
            ParentType.MOTHER: mother_node,
            ParentType.FATHER: father_node
        }
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    # Check total distributed amount with tolerance for floating-point precision
    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert abs(result.total_distributed - 1000000) < 1.0

    # Check individual shares with tolerance
    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert_share(spouse.share, 500000)    # Spouse: 1/2
    assert_share(full_sibling1.share, 125000)   # Full Sibling1: 1/8
    assert_share(nephew1.share, 125000)    # Nephew1: 1/8
    assert_share(half_sibling1.share, 125000)   # Half Sibling1: 1/8
    assert_share(half_nephew1.share, 125000)   # Half Nephew1: 1/8

def test_third_degree_with_previous_marriage_children():
    """Test case: Third Degree with Previous Marriage Children
    
    Family structure:
    - Deceased person (no children, no parents or siblings)
    - Current Spouse (alive)
    - Maternal Grandmother (alive)
    - Maternal Grandfather (deceased)
        - Uncle1 (mother's full brother, alive)
        - Uncle2 (mother's half brother from grandfather's second marriage, alive)
    - Paternal side (all deceased with no living uncles/aunts)
    
    Expected shares:
    - Current Spouse: 750,000 TL (3/4)
    Maternal side 250,000 TL (1/4):
    - Maternal Grandmother: 125,000 TL (1/8)
    - Uncle1: 62,500 TL (1/16)
    - Uncle2: 62,500 TL (1/16)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create spouse
    spouse = Person(
        id="s1",
        name="Current Spouse",
        marriage_info=MarriageInfo(marriage_order=1, is_current=True)
    )

    # Create maternal side
    maternal_grandmother = Person(
        id="mgm",
        name="Maternal Grandmother"
    )

    maternal_grandfather = Person(
        id="mgf",
        name="Maternal Grandfather",
        is_alive=False
    )

    uncle1 = Person(
        id="u1",
        name="Uncle1",
        parent_id="mgf",
        marriage_info=MarriageInfo(marriage_order=1, is_current=False)
    )

    uncle2 = Person(
        id="u2",
        name="Uncle2",
        parent_id="mgf",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    # Create family nodes
    maternal_grandfather_node = FamilyNode(
        person=maternal_grandfather,
        children=[
            FamilyNode(person=uncle1),
            FamilyNode(person=uncle2)
        ]
    )

    maternal_grandmother_node = FamilyNode(person=maternal_grandmother)

    mother_node = FamilyNode(
        person=Person(id="m1", name="Mother", is_alive=False),
        parents={
            ParentType.MOTHER: maternal_grandmother_node,
            ParentType.FATHER: maternal_grandfather_node
        }
    )

    root_node = FamilyNode(
        person=deceased,
        spouse=spouse,
        parents={
            ParentType.MOTHER: mother_node,
            ParentType.FATHER: None
        }
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    # Check total distributed amount with tolerance for floating-point precision
    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert abs(result.total_distributed - 1000000) < 1.0

    # Check individual shares with tolerance
    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert_share(spouse.share, 750000)    # Spouse: 3/4
    assert_share(maternal_grandmother.share, 125000)   # Grandmother: 1/8
    assert_share(uncle1.share, 62500)    # Uncle1: 1/16
    assert_share(uncle2.share, 62500)   # Uncle2: 1/16 

def test_second_degree_with_half_siblings():
    """Test case: Second Degree with Half-Siblings
    
    Family structure:
    - Deceased person (no children)
    - Spouse (alive)
    - Mother (alive)
    - Father (deceased)
        - Sibling1 (full sibling, alive)
        - Sibling2 (half sibling from father's second marriage, alive)
    
    Expected shares:
    - Spouse: 500,000 TL (1/2)
    - Mother: 250,000 TL (1/4)
    - Sibling1: 125,000 TL (1/8)
    - Sibling2: 125,000 TL (1/8)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create spouse
    spouse = Person(
        id="s1",
        name="Spouse"
    )

    # Create parents
    mother = Person(
        id="m1",
        name="Mother"
    )

    father = Person(
        id="f1",
        name="Father",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    # Create siblings
    sibling1 = Person(
        id="sib1",
        name="Sibling1",
        parent_id="f1"
    )

    sibling2 = Person(
        id="sib2",
        name="Sibling2",
        parent_id="f1",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    # Create family nodes for siblings
    sibling1_node = FamilyNode(person=sibling1)
    sibling2_node = FamilyNode(person=sibling2)

    # Create parent nodes
    father_node = FamilyNode(
        person=father,
        children=[sibling1_node, sibling2_node]
    )

    mother_node = FamilyNode(person=mother)

    # Create root node
    root_node = FamilyNode(
        person=deceased,
        spouse=spouse,
        parents={
            ParentType.MOTHER: mother_node,
            ParentType.FATHER: father_node
        }
    )

    # Create family tree and estate
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    assert result.total_distributed == 1000000
    assert spouse.share == 500000  # Spouse: 1/2
    assert mother.share == 250000  # Mother: 1/4
    assert sibling1.share == 125000  # Sibling1: 1/8
    assert sibling2.share == 125000  # Sibling2: 1/8

def test_complex_first_degree_multiple_marriages():
    """Test case: Complex First Degree with Multiple Marriages
    
    Family structure:
    - Deceased person
    - Current Spouse (alive)
    - Child1 (from first marriage, alive)
    - Child2 (from first marriage, deceased)
        - Grandchild1 (alive)
    - Child3 (from current marriage, alive)
    - Child4 (from current marriage, deceased)
        - Grandchild2 (alive)
        - Grandchild3 (alive)
    
    Expected shares:
    - Current Spouse: 250,000 TL (1/4)
    - Child1: 187,500 TL (3/16)
    - Grandchild1: 187,500 TL (3/16)
    - Child3: 187,500 TL (3/16)
    - Grandchild2: 93,750 TL (3/32)
    - Grandchild3: 93,750 TL (3/32)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create current spouse
    current_spouse = Person(
        id="s1",
        name="Current Spouse",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    # Create children from first marriage
    child1 = Person(
        id="c1",
        name="Child1",
        parent_id="d1",
        marriage_info=MarriageInfo(marriage_order=1, is_current=False)
    )

    child2 = Person(
        id="c2",
        name="Child2",
        parent_id="d1",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=1, is_current=False)
    )

    grandchild1 = Person(
        id="gc1",
        name="Grandchild1",
        parent_id="c2"
    )

    # Create children from current marriage
    child3 = Person(
        id="c3",
        name="Child3",
        parent_id="d1",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    child4 = Person(
        id="c4",
        name="Child4",
        parent_id="d1",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    grandchild2 = Person(
        id="gc2",
        name="Grandchild2",
        parent_id="c4"
    )

    grandchild3 = Person(
        id="gc3",
        name="Grandchild3",
        parent_id="c4"
    )

    # Create family nodes
    child2_node = FamilyNode(
        person=child2,
        children=[FamilyNode(person=grandchild1)]
    )

    child4_node = FamilyNode(
        person=child4,
        children=[
            FamilyNode(person=grandchild2),
            FamilyNode(person=grandchild3)
        ]
    )

    # Create root node
    root_node = FamilyNode(
        person=deceased,
        spouse=current_spouse,
        children=[
            FamilyNode(person=child1),
            child2_node,
            FamilyNode(person=child3),
            child4_node
        ]
    )

    # Create family tree and estate
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance

    assert result.total_distributed == 1000000
    assert_share(current_spouse.share, 250000)  # Current Spouse: 1/4
    assert_share(child1.share, 187500)  # Child1: 3/16
    assert_share(grandchild1.share, 187500)  # Grandchild1: 3/16
    assert_share(child3.share, 187500)  # Child3: 3/16
    assert_share(grandchild2.share, 93750)  # Grandchild2: 3/32
    assert_share(grandchild3.share, 93750)  # Grandchild3: 3/32 

def test_first_degree_only_children():
    """Test case: First Degree - Only Children
    
    Family structure:
    - Deceased person
    - Child1 (alive)
    - Child2 (alive)
    - Child3 (deceased)
        - Grandchild1 (alive)
        - Grandchild2 (alive)
    
    Expected shares:
    - Child1: 333,333.33 TL (1/3)
    - Child2: 333,333.33 TL (1/3)
    - Grandchild1: 166,666.67 TL (1/6)
    - Grandchild2: 166,666.67 TL (1/6)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create children
    child1 = Person(
        id="c1",
        name="Child1",
        parent_id="d1"
    )

    child2 = Person(
        id="c2",
        name="Child2",
        parent_id="d1"
    )

    child3 = Person(
        id="c3",
        name="Child3",
        parent_id="d1",
        is_alive=False
    )

    grandchild1 = Person(
        id="gc1",
        name="Grandchild1",
        parent_id="c3"
    )

    grandchild2 = Person(
        id="gc2",
        name="Grandchild2",
        parent_id="c3"
    )

    # Create family nodes
    child3_node = FamilyNode(
        person=child3,
        children=[
            FamilyNode(person=grandchild1),
            FamilyNode(person=grandchild2)
        ]
    )

    root_node = FamilyNode(
        person=deceased,
        children=[
            FamilyNode(person=child1),
            FamilyNode(person=child2),
            child3_node
        ]
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000
    assert_share(child1.share, 333333.33)  # Child1: 1/3
    assert_share(child2.share, 333333.33)  # Child2: 1/3
    assert_share(grandchild1.share, 166666.67)  # Grandchild1: 1/6
    assert_share(grandchild2.share, 166666.67)  # Grandchild2: 1/6

def test_second_degree_only_parents():
    """Test case: Second Degree - Only Parents
    
    Family structure:
    - Deceased person (no children)
    - Mother (alive)
    - Father (alive)
    
    Expected shares:
    - Mother: 500,000 TL (1/2)
    - Father: 500,000 TL (1/2)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create parents
    mother = Person(
        id="m1",
        name="Mother"
    )

    father = Person(
        id="f1",
        name="Father"
    )

    # Create family tree
    root_node = FamilyNode(
        person=deceased,
        parents={
            ParentType.MOTHER: FamilyNode(person=mother),
            ParentType.FATHER: FamilyNode(person=father)
        }
    )
    
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000
    assert_share(mother.share, 500000)  # Mother: 1/2
    assert_share(father.share, 500000)  # Father: 1/2

def test_second_degree_one_parent_with_siblings():
    """Test case: Second Degree - One Parent with Siblings
    
    Family structure:
    - Deceased person (no children)
    - Mother (alive)
    - Father (deceased)
        - Full Sibling1 (alive)
        - Full Sibling2 (alive)
        - Full Sibling3 (deceased)
            - Nephew1 (alive)
            - Nephew2 (alive)
    
    Expected shares:
    - Mother: 500,000 TL (1/2)
    - Full Sibling1: 166,666 TL (1/6)
    - Full Sibling2: 166,666 TL (1/6)
    - Nephew1: 83,333 TL (1/12)
    - Nephew2: 83,333 TL (1/12)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create parents
    mother = Person(
        id="m1",
        name="Mother"
    )

    father = Person(
        id="f1",
        name="Father",
        is_alive=False
    )

    # Create siblings
    sibling1 = Person(
        id="s1",
        name="Full Sibling1",
        parent_id="f1"
    )

    sibling2 = Person(
        id="s2",
        name="Full Sibling2",
        parent_id="f1"
    )

    sibling3 = Person(
        id="s3",
        name="Full Sibling3",
        parent_id="f1",
        is_alive=False
    )

    nephew1 = Person(
        id="n1",
        name="Nephew1",
        parent_id="s3"
    )

    nephew2 = Person(
        id="n2",
        name="Nephew2",
        parent_id="s3"
    )

    # Create family nodes
    sibling3_node = FamilyNode(
        person=sibling3,
        children=[
            FamilyNode(person=nephew1),
            FamilyNode(person=nephew2)
        ]
    )

    father_node = FamilyNode(
        person=father,
        children=[
            FamilyNode(person=sibling1),
            FamilyNode(person=sibling2),
            sibling3_node
        ]
    )

    root_node = FamilyNode(
        person=deceased,
        parents={
            ParentType.MOTHER: FamilyNode(person=mother),
            ParentType.FATHER: father_node
        }
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000
    assert_share(mother.share, 500000)  # Mother: 1/2
    assert_share(sibling1.share, 166666)  # Full Sibling1: 1/6
    assert_share(sibling2.share, 166666)  # Full Sibling2: 1/6
    assert_share(nephew1.share, 83333)  # Nephew1: 1/12
    assert_share(nephew2.share, 83333)  # Nephew2: 1/12 

def test_third_degree_only_grandparents():
    """Test case: Third Degree - Only Grandparents
    
    Family structure:
    - Deceased person (no children, no parents)
    - Maternal Grandmother (alive)
    - Maternal Grandfather (alive)
    - Paternal Grandmother (alive)
    - Paternal Grandfather (deceased)
    
    Expected shares:
    - Maternal Grandmother: 250,000 TL (1/4)
    - Maternal Grandfather: 250,000 TL (1/4)
    - Paternal Grandmother: 500,000 TL (1/2)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create maternal grandparents
    maternal_grandmother = Person(
        id="mgm",
        name="Maternal Grandmother"
    )

    maternal_grandfather = Person(
        id="mgf",
        name="Maternal Grandfather"
    )

    # Create paternal grandparents
    paternal_grandmother = Person(
        id="pgm",
        name="Paternal Grandmother"
    )

    paternal_grandfather = Person(
        id="pgf",
        name="Paternal Grandfather",
        is_alive=False
    )

    # Create family nodes
    mother_node = FamilyNode(
        person=Person(id="m1", name="Mother", is_alive=False),
        parents={
            ParentType.MOTHER: FamilyNode(person=maternal_grandmother),
            ParentType.FATHER: FamilyNode(person=maternal_grandfather)
        }
    )

    father_node = FamilyNode(
        person=Person(id="f1", name="Father", is_alive=False),
        parents={
            ParentType.MOTHER: FamilyNode(person=paternal_grandmother),
            ParentType.FATHER: FamilyNode(person=paternal_grandfather)
        }
    )

    root_node = FamilyNode(
        person=deceased,
        parents={
            ParentType.MOTHER: mother_node,
            ParentType.FATHER: father_node
        }
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000
    assert_share(maternal_grandmother.share, 250000)  # Maternal Grandmother: 1/4
    assert_share(maternal_grandfather.share, 250000)  # Maternal Grandfather: 1/4
    assert_share(paternal_grandmother.share, 500000)  # Paternal Grandmother: 1/2

def test_third_degree_grandparents_and_uncles():
    """Test case: Third Degree - Grandparents and Uncles
    
    Family structure:
    - Deceased person (no children, no parents)
    - Maternal Grandmother (alive)
    - Maternal Grandfather (deceased)
        - Uncle1 (mother's brother, alive)
        - Uncle2 (mother's brother, deceased)
            - Cousin1 (alive)
            - Cousin2 (alive)
    - Paternal side (all deceased, no heirs)
    
    Expected shares:
    - Maternal Grandmother: 500,000 TL (1/2)
    - Uncle1: 500,000 TL (1/2)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create maternal grandparents
    maternal_grandmother = Person(
        id="mgm",
        name="Maternal Grandmother"
    )

    maternal_grandfather = Person(
        id="mgf",
        name="Maternal Grandfather",
        is_alive=False
    )

    # Create uncles
    uncle1 = Person(
        id="u1",
        name="Uncle1",
        parent_id="mgf"
    )

    uncle2 = Person(
        id="u2",
        name="Uncle2",
        parent_id="mgf",
        is_alive=False
    )

    cousin1 = Person(
        id="c1",
        name="Cousin1",
        parent_id="u2"
    )

    cousin2 = Person(
        id="c2",
        name="Cousin2",
        parent_id="u2"
    )

    # Create family nodes
    uncle2_node = FamilyNode(
        person=uncle2,
        children=[
            FamilyNode(person=cousin1),
            FamilyNode(person=cousin2)
        ]
    )

    maternal_grandfather_node = FamilyNode(
        person=maternal_grandfather,
        children=[
            FamilyNode(person=uncle1),
            uncle2_node
        ]
    )

    mother_node = FamilyNode(
        person=Person(id="m1", name="Mother", is_alive=False),
        parents={
            ParentType.MOTHER: FamilyNode(person=maternal_grandmother),
            ParentType.FATHER: maternal_grandfather_node
        }
    )

    root_node = FamilyNode(
        person=deceased,
        parents={
            ParentType.MOTHER: mother_node,
            ParentType.FATHER: None
        }
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000
    assert_share(maternal_grandmother.share, 500000)  # Maternal Grandmother: 1/2
    assert_share(uncle1.share, 500000)  # Uncle1: 1/2

def test_first_degree_complex_multiple_lines():
    """Test case: First Degree - Complex Multiple Lines
    
    Family structure:
    - Deceased person
    - Child1 (alive)
    - Child2 (deceased)
        - Grandchild1 (alive)
        - Grandchild2 (deceased)
            - Great-grandchild1 (alive)
            - Great-grandchild2 (alive)
    - Child3 (deceased)
        - Grandchild3 (alive)
        - Grandchild4 (alive)
        - Grandchild5 (alive)
    
    Expected shares:
    - Child1: 333,333.33 TL (1/3)
    - Grandchild1: 166,666.67 TL (1/6)
    - Great-grandchild1: 83,333.33 TL (1/12)
    - Great-grandchild2: 83,333.33 TL (1/12)
    - Grandchild3: 111,111.11 TL (1/9)
    - Grandchild4: 111,111.11 TL (1/9)
    - Grandchild5: 111,111.11 TL (1/9)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create first line
    child1 = Person(
        id="c1",
        name="Child1",
        parent_id="d1"
    )

    # Create second line
    child2 = Person(
        id="c2",
        name="Child2",
        parent_id="d1",
        is_alive=False
    )

    grandchild1 = Person(
        id="gc1",
        name="Grandchild1",
        parent_id="c2"
    )

    grandchild2 = Person(
        id="gc2",
        name="Grandchild2",
        parent_id="c2",
        is_alive=False
    )

    great_grandchild1 = Person(
        id="ggc1",
        name="Great-grandchild1",
        parent_id="gc2"
    )

    great_grandchild2 = Person(
        id="ggc2",
        name="Great-grandchild2",
        parent_id="gc2"
    )

    # Create third line
    child3 = Person(
        id="c3",
        name="Child3",
        parent_id="d1",
        is_alive=False
    )

    grandchild3 = Person(
        id="gc3",
        name="Grandchild3",
        parent_id="c3"
    )

    grandchild4 = Person(
        id="gc4",
        name="Grandchild4",
        parent_id="c3"
    )

    grandchild5 = Person(
        id="gc5",
        name="Grandchild5",
        parent_id="c3"
    )

    # Create family nodes
    grandchild2_node = FamilyNode(
        person=grandchild2,
        children=[
            FamilyNode(person=great_grandchild1),
            FamilyNode(person=great_grandchild2)
        ]
    )

    child2_node = FamilyNode(
        person=child2,
        children=[
            FamilyNode(person=grandchild1),
            grandchild2_node
        ]
    )

    child3_node = FamilyNode(
        person=child3,
        children=[
            FamilyNode(person=grandchild3),
            FamilyNode(person=grandchild4),
            FamilyNode(person=grandchild5)
        ]
    )

    root_node = FamilyNode(
        person=deceased,
        children=[
            FamilyNode(person=child1),
            child2_node,
            child3_node
        ]
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) <= 1.0, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000
    assert_share(child1.share, 333333.33)  # Child1: 1/3
    assert_share(grandchild1.share, 166666.67)  # Grandchild1: 1/6
    assert_share(great_grandchild1.share, 83333.33)  # Great-grandchild1: 1/12
    assert_share(great_grandchild2.share, 83333.33)  # Great-grandchild2: 1/12
    assert_share(grandchild3.share, 111111.11)  # Grandchild3: 1/9
    assert_share(grandchild4.share, 111111.11)  # Grandchild4: 1/9
    assert_share(grandchild5.share, 111111.11)  # Grandchild5: 1/9

def test_second_degree_complex_mixed_siblings():
    """Test case: Second Degree - Complex Mixed Siblings
    Don't forget on third degree aunts and uncles children are not included in the inheritance

    Family structure:
    - Deceased person (no children)
    - Mother (deceased)
        - Full Sibling1 (alive)
        - Full Sibling2 (deceased)
            - Nephew1 (alive)
            - Nephew2 (deceased)
                - Grand-nephew1 (alive)
    - Father (deceased)
        - Half Sibling1 (from second marriage, alive)
        - Half Sibling2 (from second marriage, deceased)
            - Half Nephew1 (alive)
            - Half Nephew2 (alive)
    
    Expected shares:
    - Full Sibling1: 250,000 TL (1/4)
    - Nephew1: 125,000 TL (1/8)
    - Grand-nephew1: 125,000 TL (1/8)
    - Half Sibling1: 250,000 TL (1/4)
    - Half Nephew1: 125,000 TL (1/8)
    - Half Nephew2: 125,000 TL (1/8)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create mother's side
    mother = Person(
        id="m1",
        name="Mother",
        is_alive=False
    )

    full_sibling1 = Person(
        id="fs1",
        name="Full Sibling1",
        parent_id="m1"
    )

    full_sibling2 = Person(
        id="fs2",
        name="Full Sibling2",
        parent_id="m1",
        is_alive=False
    )

    nephew1 = Person(
        id="n1",
        name="Nephew1",
        parent_id="fs2"
    )

    nephew2 = Person(
        id="n2",
        name="Nephew2",
        parent_id="fs2",
        is_alive=False
    )

    grand_nephew1 = Person(
        id="gn1",
        name="Grand-nephew1",
        parent_id="n2"
    )

    # Create father's side
    father = Person(
        id="f1",
        name="Father",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    half_sibling1 = Person(
        id="hs1",
        name="Half Sibling1",
        parent_id="f1",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    half_sibling2 = Person(
        id="hs2",
        name="Half Sibling2",
        parent_id="f1",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    half_nephew1 = Person(
        id="hn1",
        name="Half Nephew1",
        parent_id="hs2"
    )

    half_nephew2 = Person(
        id="hn2",
        name="Half Nephew2",
        parent_id="hs2"
    )

    # Create family nodes
    nephew2_node = FamilyNode(
        person=nephew2,
        children=[FamilyNode(person=grand_nephew1)]
    )

    full_sibling2_node = FamilyNode(
        person=full_sibling2,
        children=[
            FamilyNode(person=nephew1),
            nephew2_node
        ]
    )

    half_sibling2_node = FamilyNode(
        person=half_sibling2,
        children=[
            FamilyNode(person=half_nephew1),
            FamilyNode(person=half_nephew2)
        ]
    )

    mother_node = FamilyNode(
        person=mother,
        children=[
            FamilyNode(person=full_sibling1),
            full_sibling2_node
        ]
    )

    father_node = FamilyNode(
        person=father,
        children=[
            FamilyNode(person=half_sibling1),
            half_sibling2_node
        ]
    )

    root_node = FamilyNode(
        person=deceased,
        parents={
            ParentType.MOTHER: mother_node,
            ParentType.FATHER: father_node
        }
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000
    assert_share(full_sibling1.share, 250000)  # Full Sibling1: 1/4
    assert_share(nephew1.share, 125000)  # Nephew1: 1/8
    assert_share(grand_nephew1.share, 125000)  # Grand-nephew1: 1/8
    assert_share(half_sibling1.share, 250000)  # Half Sibling1: 1/4
    assert_share(half_nephew1.share, 125000)  # Half Nephew1: 1/8
    assert_share(half_nephew2.share, 125000)  # Half Nephew2: 1/8 

def test_third_degree_complex_mixed_uncles():
    """Test case: Third Degree - Complex Mixed Uncles or aunts
    Don't forget on third degree aunts and uncles children are not included in the inheritance

    Family structure:
    - Deceased person (no children, no parents)
    - Maternal Grandmother (alive)
    - Maternal Grandfather (deceased)
        - Uncle1 (mother's full brother, alive)
        - Uncle2 (mother's full brother, deceased)
            - Cousin1 (alive)
            - Cousin2 (deceased)
                - Second Cousin1 (alive)
        - Uncle3 (mother's half brother from second marriage, alive)
        - Uncle4 (mother's half brother from second marriage, deceased)
            - Cousin3 (alive)
    - Paternal Grandmother (deceased)
    - Paternal Grandfather (deceased)
        - Uncle5 (father's brother, alive)
        - Uncle6 (father's brother, deceased)
            - Cousin4 (alive)
            - Cousin5 (alive)
    
    Expected shares:
    Maternal side 500,000 TL (1/2):
    - Maternal Grandmother: 250,000 TL (1/4)
    - Uncle1: 125,000 TL (1/8)
    - Uncle3: 125,000 TL (1/8)
    Paternal side 500,000 TL (1/2):
    - Uncle5: 500,000 TL (1/2)
    """
    # Create the deceased person
    deceased = Person(
        id="d1",
        name="Deceased",
        is_alive=False
    )

    # Create maternal side
    maternal_grandmother = Person(
        id="mgm",
        name="Maternal Grandmother"
    )

    maternal_grandfather = Person(
        id="mgf",
        name="Maternal Grandfather",
        is_alive=False
    )

    uncle1 = Person(
        id="u1",
        name="Uncle1",
        parent_id="mgf"
    )

    uncle2 = Person(
        id="u2",
        name="Uncle2",
        parent_id="mgf",
        is_alive=False
    )

    cousin1 = Person(
        id="c1",
        name="Cousin1",
        parent_id="u2"
    )

    cousin2 = Person(
        id="c2",
        name="Cousin2",
        parent_id="u2",
        is_alive=False
    )

    second_cousin1 = Person(
        id="sc1",
        name="Second Cousin1",
        parent_id="c2"
    )

    uncle3 = Person(
        id="u3",
        name="Uncle3",
        parent_id="mgf",
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    uncle4 = Person(
        id="u4",
        name="Uncle4",
        parent_id="mgf",
        is_alive=False,
        marriage_info=MarriageInfo(marriage_order=2, is_current=True)
    )

    cousin3 = Person(
        id="c3",
        name="Cousin3",
        parent_id="u4"
    )

    # Create paternal side
    paternal_grandmother = Person(
        id="pgm",
        name="Paternal Grandmother",
        is_alive=False
    )

    paternal_grandfather = Person(
        id="pgf",
        name="Paternal Grandfather",
        is_alive=False
    )

    uncle5 = Person(
        id="u5",
        name="Uncle5",
        parent_id="pgf"
    )

    uncle6 = Person(
        id="u6",
        name="Uncle6",
        parent_id="pgf",
        is_alive=False
    )

    cousin4 = Person(
        id="c4",
        name="Cousin4",
        parent_id="u6"
    )

    cousin5 = Person(
        id="c5",
        name="Cousin5",
        parent_id="u6"
    )

    # Create family nodes
    cousin2_node = FamilyNode(
        person=cousin2,
        children=[FamilyNode(person=second_cousin1)]
    )

    uncle2_node = FamilyNode(
        person=uncle2,
        children=[
            FamilyNode(person=cousin1),
            cousin2_node
        ]
    )

    uncle4_node = FamilyNode(
        person=uncle4,
        children=[FamilyNode(person=cousin3)]
    )

    uncle6_node = FamilyNode(
        person=uncle6,
        children=[
            FamilyNode(person=cousin4),
            FamilyNode(person=cousin5)
        ]
    )

    maternal_grandfather_node = FamilyNode(
        person=maternal_grandfather,
        children=[
            FamilyNode(person=uncle1),
            uncle2_node,
            FamilyNode(person=uncle3),
            uncle4_node
        ]
    )

    paternal_grandfather_node = FamilyNode(
        person=paternal_grandfather,
        children=[
            FamilyNode(person=uncle5),
            uncle6_node
        ]
    )

    mother_node = FamilyNode(
        person=Person(id="m1", name="Mother", is_alive=False),
        parents={
            ParentType.MOTHER: FamilyNode(person=maternal_grandmother),
            ParentType.FATHER: maternal_grandfather_node
        }
    )

    father_node = FamilyNode(
        person=Person(id="f1", name="Father", is_alive=False),
        parents={
            ParentType.MOTHER: FamilyNode(person=paternal_grandmother),
            ParentType.FATHER: paternal_grandfather_node
        }
    )

    root_node = FamilyNode(
        person=deceased,
        parents={
            ParentType.MOTHER: mother_node,
            ParentType.FATHER: father_node
        }
    )

    # Create family tree
    family_tree = FamilyTree(root=root_node)
    estate = Estate(total_value=1000000, family_tree=family_tree)

    # Calculate inheritance
    calculator = InheritanceCalculator(estate)
    result = calculator.calculate()

    def assert_share(actual: float, expected: float, tolerance: float = 1.0):
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"

    assert result.total_distributed == 1000000


    # Maternal side
    assert_share(maternal_grandmother.share, 250000)  # Maternal Grandmother: 1/4
    assert_share(uncle1.share, 125000)  # Uncle1: 1/8
    assert_share(uncle3.share, 125000)  # Uncle3: 1/8
    # Paternal side
    assert_share(uncle5.share, 500000)  # Uncle5: 1/2
