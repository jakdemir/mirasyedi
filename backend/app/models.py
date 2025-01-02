from pydantic import BaseModel
from typing import List, Optional

class Heir(BaseModel):
    name: str
    relation: str  # e.g., 'spouse', 'child', 'parent', etc.
    share: Optional[float] = 0.0  # Initialize share to 0.0
    children: Optional[List['Heir']] = []  # Nested structure for family tree

class Estate(BaseModel):
    total_value: float
    heirs: List[Heir]  # List of all heirs
