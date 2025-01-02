from pydantic import BaseModel
from typing import List, Optional

class Heir(BaseModel):
    name: str
    relation: str  # Relation to the deceased (e.g., "spouse", "child")
    share: Optional[float] = 0.0  # Share of the inheritance (to be calculated)

class Estate(BaseModel):
    total_value: float  # Total value of the inheritance
    heirs: List[Heir]  # List of heirs
