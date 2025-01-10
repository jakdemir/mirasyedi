from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel

class ParentType(str, Enum):
    MOTHER = "mother"
    FATHER = "father"

class MarriageInfo(BaseModel):
    marriage_order: int = 1
    is_current: bool = True

class Person(BaseModel):
    """Base class for representing a person in the family tree."""
    id: str
    name: str
    is_alive: bool = True
    marriage_info: Optional[MarriageInfo] = None
    parent_id: Optional[str] = None
    share: float = 0
    share_ratio: float = 0

    def get_share(self) -> float:
        """Get this person's share of the inheritance."""
        return self.share

class FamilyNode(BaseModel):
    """Represents a node in the family tree."""
    person: Person
    spouse: Optional[Person] = None
    children: List['FamilyNode'] = []
    parents: Dict[ParentType, Optional['FamilyNode']] = {
        ParentType.MOTHER: None,
        ParentType.FATHER: None
    }

    def get_living_descendants(self) -> List[Person]:
        """Get all living descendants in this subtree."""
        descendants = []
        for child_node in self.children:
            if child_node.person.is_alive:
                descendants.append(child_node.person)
            descendants.extend(child_node.get_living_descendants())
        return descendants

    def get_living_siblings(self) -> List[Person]:
        """Get all living siblings (including half-siblings) and their descendants if the sibling is deceased."""
        siblings = []
        for parent_node in self.parents.values():
            if parent_node:
                for sibling_node in parent_node.children:
                    if sibling_node.person.id != self.person.id:
                        if sibling_node.person.is_alive:
                            siblings.append(sibling_node.person)
                        else:
                            # Add living children of deceased siblings
                            for child_node in sibling_node.children:
                                if child_node.person.is_alive:
                                    child_node.person.parent_id = sibling_node.person.id
                                    siblings.append(child_node.person)
        return list({s.id: s for s in siblings}.values())  # Remove duplicates

    def get_living_parents(self) -> List[Person]:
        """Get living parents."""
        return [p.person for p in self.parents.values() if p and p.person.is_alive]

    def get_living_grandparents(self) -> List[Person]:
        """Get living grandparents."""
        grandparents = []
        for parent_node in self.parents.values():
            if parent_node:
                grandparents.extend(parent_node.get_living_parents())
        return grandparents

    def get_living_uncles(self) -> List[Person]:
        """Get living uncles/aunts."""
        uncles = []
        for parent_node in self.parents.values():
            if parent_node:
                uncles.extend(parent_node.get_living_siblings())
        return uncles

    def get_living_heirs(self) -> List[Person]:
        """Get all living heirs in this subtree."""
        heirs = []
        
        # Add spouse if alive
        if self.spouse and self.spouse.is_alive:
            self.spouse.share = 0  # Reset share
            heirs.append(self.spouse)

        # Add living descendants
        descendants = self.get_living_descendants()
        for descendant in descendants:
            descendant.share = 0  # Reset share
        heirs.extend(descendants)

        # If no descendants, add parents and their descendants
        if not descendants:
            parents = self.get_living_parents()
            for parent in parents:
                parent.share = 0  # Reset share
            heirs.extend(parents)

            if len(parents) < 2:  # If not both parents are alive
                siblings = self.get_living_siblings()
                for sibling in siblings:
                    sibling.share = 0  # Reset share
                heirs.extend(siblings)

            # If no parents or siblings, add grandparents and uncles
            if not (parents or siblings):
                grandparents = self.get_living_grandparents()
                for grandparent in grandparents:
                    grandparent.share = 0  # Reset share
                heirs.extend(grandparents)

                uncles = self.get_living_uncles()
                for uncle in uncles:
                    uncle.share = 0  # Reset share
                heirs.extend(uncles)

        return heirs

class FamilyTree(BaseModel):
    """Represents the entire family tree with the deceased person as the root."""
    root: FamilyNode

    def get_living_heirs(self) -> List[Person]:
        """Get all living heirs in the family tree."""
        return self.root.get_living_heirs()

class Estate(BaseModel):
    """Represents the estate to be distributed."""
    total_value: float
    family_tree: FamilyTree

class InheritanceResult(BaseModel):
    """Represents the result of inheritance calculation."""
    estate: Estate
    total_distributed: float
    explanation: str 