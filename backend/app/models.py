from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class RelationType(str, Enum):
    SPOUSE = "spouse"
    PARENT = "parent"
    GRANDPARENT = "grandparent"
    CHILD = "child"

class Heir(BaseModel):
    name: str
    relation: RelationType  # Using enum to restrict relationship types
    is_alive: bool = True
    share: Optional[float] = 0.0
    children: Optional[List['Heir']] = []
    side: Optional[str] = None  # 'maternal' or 'paternal'
    parent: Optional[str] = None  # Name of the parent

class Estate(BaseModel):
    total_value: float
    heirs: List[Heir]
