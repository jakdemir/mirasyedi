from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from .models import Estate, FamilyTree, FamilyNode, Person, ParentType, MarriageInfo
from .calculations import InheritanceCalculator

app = FastAPI(title="Inheritance Distribution Calculator")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MarriageInfoSchema(BaseModel):
    marriage_order: int
    is_current: bool

class PersonSchema(BaseModel):
    id: str
    name: str
    is_alive: bool = True
    parent_id: Optional[str] = None
    marriage_info: Optional[MarriageInfoSchema] = None
    share: float = 0

class FamilyNodeSchema(BaseModel):
    person: PersonSchema
    spouse: Optional[PersonSchema] = None
    children: List['FamilyNodeSchema'] = []
    parents: Optional[Dict[str, 'FamilyNodeSchema']] = None

    class Config:
        schema_extra = {
            "example": {
                "person": {
                    "id": "d1",
                    "name": "Deceased",
                    "is_alive": False
                },
                "spouse": {
                    "id": "s1",
                    "name": "Spouse",
                    "is_alive": True
                },
                "children": [
                    {
                        "person": {
                            "id": "c1",
                            "name": "Child1",
                            "is_alive": True,
                            "parent_id": "d1"
                        }
                    }
                ]
            }
        }

class InheritanceRequest(BaseModel):
    estate_value: float = Field(..., gt=0, description="Total value of the estate")
    family_tree: FamilyNodeSchema

    class Config:
        schema_extra = {
            "example": {
                "estate_value": 1000000,
                "family_tree": {
                    "person": {
                        "id": "d1",
                        "name": "Deceased",
                        "is_alive": False
                    },
                    "spouse": {
                        "id": "s1",
                        "name": "Spouse",
                        "is_alive": True
                    },
                    "children": [
                        {
                            "person": {
                                "id": "c1",
                                "name": "Child1",
                                "is_alive": True,
                                "parent_id": "d1"
                            }
                        }
                    ]
                }
            }
        }

class InheritanceResponse(BaseModel):
    total_distributed: float
    shares: Dict[str, float]

def convert_schema_to_model(node_schema: FamilyNodeSchema) -> FamilyNode:
    """Convert FamilyNodeSchema to FamilyNode model"""
    # Convert person
    person = Person(
        id=node_schema.person.id,
        name=node_schema.person.name,
        is_alive=node_schema.person.is_alive,
        parent_id=node_schema.person.parent_id
    )
    if node_schema.person.marriage_info:
        person.marriage_info = MarriageInfo(
            marriage_order=node_schema.person.marriage_info.marriage_order,
            is_current=node_schema.person.marriage_info.is_current
        )

    # Convert spouse if exists
    spouse = None
    if node_schema.spouse:
        spouse = Person(
            id=node_schema.spouse.id,
            name=node_schema.spouse.name,
            is_alive=node_schema.spouse.is_alive,
            parent_id=node_schema.spouse.parent_id
        )
        if node_schema.spouse.marriage_info:
            spouse.marriage_info = MarriageInfo(
                marriage_order=node_schema.spouse.marriage_info.marriage_order,
                is_current=node_schema.spouse.marriage_info.is_current
            )

    # Convert children
    children = [convert_schema_to_model(child) for child in node_schema.children]

    # Convert parents
    parents = {}
    if node_schema.parents:
        for parent_type_str, parent_node in node_schema.parents.items():
            if parent_node:
                # Convert string to ParentType enum
                if parent_type_str.upper() == "MOTHER":
                    parent_type = ParentType.MOTHER
                elif parent_type_str.upper() == "FATHER":
                    parent_type = ParentType.FATHER
                else:
                    raise ValueError(f"Invalid parent type: {parent_type_str}")
                parents[parent_type] = convert_schema_to_model(parent_node)

    return FamilyNode(
        person=person,
        spouse=spouse,
        children=children,
        parents=parents
    )

@app.post("/calculate")
async def calculate_inheritance(request: InheritanceRequest) -> InheritanceResponse:
    try:
        calculator = InheritanceCalculator()
        estate = Estate(value=request.estate_value)
        family_tree = FamilyTree(root=request.family_tree)
        
        shares = calculator.calculate_shares(estate, family_tree)
        return InheritanceResponse(
            total_distributed=estate.value,
            shares=shares
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 