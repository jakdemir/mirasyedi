from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict
from enum import Enum

class RelationType(str, Enum):
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    GRANDPARENT = "grandparent"

class FamilyBranch(str, Enum):
    DIRECT = "direct"
    MATERNAL = "maternal"
    PATERNAL = "paternal"

class ParentType(str, Enum):
    MOTHER = "mother"
    FATHER = "father"

class Person(BaseModel):
    id: str  # Unique identifier for the person
    name: str
    is_alive: bool = True
    share: float = 0.0

class Heir(BaseModel):
    id: str
    name: str
    relation: RelationType
    is_alive: bool = True
    share: float = 0
    branch: FamilyBranch = FamilyBranch.DIRECT
    parent_id: Optional[str] = None
    children: List['Heir'] = []
    generation: Optional[int] = None
    parent_type: Optional[ParentType] = None  # New field to specify if the heir is a mother or father

    model_config = ConfigDict(validate_assignment=True)

    def add_child(self, child: 'Heir') -> None:
        """Add a child to this heir"""
        child.parent_id = self.id
        self.children.append(child)

    def get_descendants(self) -> List['Heir']:
        """Get all descendants of this heir"""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def get_living_descendants(self) -> List['Heir']:
        """Get all living descendants of this heir"""
        return [heir for heir in self.get_descendants() if heir.is_alive]

    def get_children_by_relation(self, relation: RelationType) -> List['Heir']:
        """Get all children with a specific relation type"""
        return [child for child in self.children if child.relation == relation]

class FamilyTree(BaseModel):
    spouse: Optional[Heir] = None
    children: List[Heir] = []
    mother: Optional[Heir] = None
    father: Optional[Heir] = None
    maternal_grandparents: List[Heir] = []
    paternal_grandparents: List[Heir] = []

    def add_heir(self, heir: Heir) -> None:
        """Add an heir to the family tree."""
        if heir.relation == RelationType.SPOUSE:
            self.spouse = heir
        elif heir.relation == RelationType.PARENT:
            if heir.parent_type == ParentType.MOTHER:
                self.mother = heir
            elif heir.parent_type == ParentType.FATHER:
                self.father = heir
        elif heir.branch == FamilyBranch.MATERNAL:
            self.maternal_grandparents.append(heir)
        elif heir.branch == FamilyBranch.PATERNAL:
            self.paternal_grandparents.append(heir)
        elif heir.branch == FamilyBranch.DIRECT:
            self.children.append(heir)

    def get_all_heirs(self) -> List[Heir]:
        """Get all heirs in the family tree, including descendants"""
        heirs = []
        if self.spouse:
            heirs.append(self.spouse)
            heirs.extend(self.spouse.get_descendants())
        
        if self.mother:
            heirs.append(self.mother)
            heirs.extend(self.mother.get_descendants())
        
        if self.father:
            heirs.append(self.father)
            heirs.extend(self.father.get_descendants())
        
        for child in self.children:
            heirs.append(child)
            heirs.extend(child.get_descendants())
        
        for gp in self.maternal_grandparents:
            heirs.append(gp)
            heirs.extend(gp.get_descendants())
        
        for gp in self.paternal_grandparents:
            heirs.append(gp)
            heirs.extend(gp.get_descendants())
        
        return heirs

    def get_living_heirs(self) -> List[Heir]:
        """Get all living heirs in the family tree"""
        return [heir for heir in self.get_all_heirs() if heir.is_alive]

    def get_heirs_by_relation(self, relation: RelationType) -> List[Heir]:
        """Get all heirs with a specific relation type"""
        return [heir for heir in self.get_all_heirs() if heir.relation == relation]

    def get_branch_heirs(self, branch: FamilyBranch) -> List[Heir]:
        """Get all heirs in a specific branch"""
        if branch == FamilyBranch.DIRECT:
            return self.children
        elif branch == FamilyBranch.MATERNAL:
            return self.maternal_grandparents
        elif branch == FamilyBranch.PATERNAL:
            return self.paternal_grandparents
        return []

class Estate(BaseModel):
    total_value: float
    family_tree: FamilyTree

    model_config = ConfigDict(validate_assignment=True)
