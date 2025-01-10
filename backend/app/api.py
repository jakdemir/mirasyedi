from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Union
from enum import Enum
from .models import Estate, FamilyTree, FamilyNode, Person, ParentType, MarriageInfo
from .calculations import InheritanceCalculator
import logging

# Configure logger
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Turkish Inheritance Calculator API",
    description="API for calculating inheritance distribution according to Turkish Civil Law",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RelativeType(str, Enum):
    SPOUSE = "spouse"
    CHILD = "child"
    PARENT = "parent"
    SIBLING = "sibling"
    GRANDPARENT = "grandparent"

class MarriageInfoSchema(BaseModel):
    marriage_order: int = Field(ge=1, description="Order of marriage (1 for first marriage, etc.)")
    is_current: bool = Field(default=True, description="Whether this is the current marriage")

    class Config:
        schema_extra = {
            "example": {
                "marriage_order": 1,
                "is_current": True
            }
        }

class PersonSchema(BaseModel):
    id: str = Field(..., description="Unique identifier for the person")
    name: str = Field(..., min_length=1, description="Full name of the person")
    is_alive: bool = Field(default=True, description="Whether the person is alive")
    parent_id: Optional[str] = Field(None, description="ID of the parent (if applicable)")
    marriage_info: Optional[MarriageInfoSchema] = Field(None, description="Marriage information (if applicable)")
    share: float = Field(default=0, description="Share of the inheritance")
    share_percentage: Optional[float] = Field(None, description="Percentage of the total inheritance")

    class Config:
        schema_extra = {
            "example": {
                "id": "p1",
                "name": "John Doe",
                "is_alive": True,
                "parent_id": None,
                "marriage_info": {
                    "marriage_order": 1,
                    "is_current": True
                },
                "share": 0,
                "share_percentage": 0
            }
        }

class FamilyNodeSchema(BaseModel):
    person: PersonSchema
    spouse: Optional[PersonSchema] = Field(None, description="Spouse information")
    children: List['FamilyNodeSchema'] = Field(default_factory=list, description="List of children")
    parents: Optional[Dict[str, 'FamilyNodeSchema']] = Field(None, description="Parent information")

    class Config:
        schema_extra = {
            "example": {
                "person": {
                    "id": "d1",
                    "name": "Deceased Person",
                    "is_alive": False
                },
                "spouse": {
                    "id": "s1",
                    "name": "Spouse",
                    "is_alive": True,
                    "marriage_info": {
                        "marriage_order": 1,
                        "is_current": True
                    }
                },
                "children": [
                    {
                        "person": {
                            "id": "c1",
                            "name": "Child 1",
                            "is_alive": True,
                            "parent_id": "d1"
                        }
                    }
                ]
            }
        }

class InheritanceRequest(BaseModel):
    estate_value: float = Field(..., gt=0, description="Total value of the estate in TRY")
    family_tree: FamilyNodeSchema

    @validator('estate_value')
    def validate_estate_value(cls, v):
        if v <= 0:
            raise ValueError("Estate value must be greater than 0")
        return v

    class Config:
        schema_extra = {
            "example": {
                "estate_value": 1000000,
                "family_tree": {
                    "person": {
                        "id": "d1",
                        "name": "Deceased Person",
                        "is_alive": False
                    },
                    "spouse": {
                        "id": "s1",
                        "name": "Spouse",
                        "is_alive": True,
                        "marriage_info": {
                            "marriage_order": 1,
                            "is_current": True
                        }
                    },
                    "children": [
                        {
                            "person": {
                                "id": "c1",
                                "name": "Child 1",
                                "is_alive": True,
                                "parent_id": "d1"
                            }
                        }
                    ]
                }
            }
        }

class StructuredInheritanceResponse(BaseModel):
    total_distributed: float = Field(..., description="Total amount distributed from the estate")
    family_tree: FamilyNodeSchema = Field(..., description="Family tree with inheritance shares")
    summary: Dict[str, Dict[str, Union[str, float]]] = Field(
        ..., 
        description="Summary of inheritance distribution by person"
    )

    class Config:
        schema_extra = {
            "example": {
                "total_distributed": 1000000,
                "family_tree": {
                    "person": {
                        "id": "d1",
                        "name": "Deceased Person",
                        "is_alive": False,
                        "share": 0,
                        "share_percentage": 0
                    },
                    "spouse": {
                        "id": "s1",
                        "name": "Spouse",
                        "is_alive": True,
                        "share": 250000,
                        "share_percentage": 25
                    },
                    "children": [
                        {
                            "person": {
                                "id": "c1",
                                "name": "Child 1",
                                "is_alive": True,
                                "share": 750000,
                                "share_percentage": 75
                            }
                        }
                    ]
                },
                "summary": {
                    "s1": {
                        "name": "Spouse",
                        "relation": "spouse",
                        "share": 250000,
                        "share_percentage": 25
                    },
                    "c1": {
                        "name": "Child 1",
                        "relation": "child",
                        "share": 750000,
                        "share_percentage": 75
                    }
                }
            }
        }

def update_node_with_shares(
    node: FamilyNodeSchema, 
    shares: Dict[str, float], 
    total_distributed: float
) -> None:
    """Update a family node and its descendants with their inheritance shares"""
    # Update person's share
    if node.person.id in shares:
        node.person.share = shares[node.person.id]
        node.person.share_percentage = (shares[node.person.id] / total_distributed) * 100

    # Update spouse's share
    if node.spouse and node.spouse.id in shares:
        node.spouse.share = shares[node.spouse.id]
        node.spouse.share_percentage = (shares[node.spouse.id] / total_distributed) * 100

    # Update children's shares
    for child in node.children:
        update_node_with_shares(child, shares, total_distributed)

    # Update parents' shares
    if node.parents:
        for parent in node.parents.values():
            if parent:
                update_node_with_shares(parent, shares, total_distributed)

def create_inheritance_summary(
    node: FamilyNodeSchema,
    shares: Dict[str, float],
    total_distributed: float,
    summary: Dict[str, Dict[str, Union[str, float]]] = None,
    relation: str = None
) -> Dict[str, Dict[str, Union[str, float]]]:
    """Create a summary of inheritance distribution"""
    if summary is None:
        summary = {}

    # Add person if they have a share
    if node.person.id in shares:
        summary[node.person.id] = {
            "name": node.person.name,
            "relation": relation or "deceased",
            "share": shares[node.person.id],
            "share_percentage": (shares[node.person.id] / total_distributed) * 100
        }

    # Add spouse if they have a share
    if node.spouse and node.spouse.id in shares:
        summary[node.spouse.id] = {
            "name": node.spouse.name,
            "relation": "spouse",
            "share": shares[node.spouse.id],
            "share_percentage": (shares[node.spouse.id] / total_distributed) * 100
        }

    # Process children
    for child in node.children:
        create_inheritance_summary(child, shares, total_distributed, summary, "child")

    # Process parents
    if node.parents:
        for parent_type, parent in node.parents.items():
            if parent:
                create_inheritance_summary(parent, shares, total_distributed, summary, parent_type)

    return summary

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "title": "Turkish Inheritance Calculator API",
        "version": "1.0.0",
        "description": "Calculate inheritance distribution according to Turkish Civil Law"
    }

@app.get("/relative-types")
async def get_relative_types():
    """Get available relative types"""
    return {
        "relative_types": [type.value for type in RelativeType]
    }

@app.post("/calculate", response_model=StructuredInheritanceResponse)
async def calculate_inheritance(
    request: InheritanceRequest,
) -> StructuredInheritanceResponse:
    """
    Calculate inheritance distribution based on the provided family tree and estate value.
    
    The calculation follows Turkish Civil Law rules for inheritance distribution.
    Returns the distribution in the context of the family tree structure.
    """
    try:
        logger.info(f"Received calculation request for estate value: {request.estate_value}")
        logger.debug(f"Full request data: {request.dict()}")

        # Convert schema to model
        logger.debug("Converting schema to model...")
        root_node = convert_schema_to_model(request.family_tree)
        logger.debug(f"Root node created: {root_node}")
        
        # Create estate and family tree
        logger.debug("Creating estate and family tree...")
        family_tree = FamilyTree(root=root_node)
        estate = Estate(total_value=request.estate_value, family_tree=family_tree)
        logger.debug(f"Estate created with value: {estate.total_value}")
        
        # Calculate inheritance
        logger.info("Calculating inheritance shares...")
        calculator = InheritanceCalculator(estate=estate)
        result = calculator.calculate()
        logger.debug(f"Calculation result: {result}")
        
        # Get shares from the nodes
        shares = {}
        def collect_shares(node: FamilyNode):
            if node.person and node.person.share > 0:
                shares[node.person.id] = node.person.share
            if node.spouse and node.spouse.share > 0:
                shares[node.spouse.id] = node.spouse.share
            for child in node.children:
                collect_shares(child)
            if node.parents:
                for parent in node.parents.values():
                    if parent:
                        collect_shares(parent)
        
        collect_shares(root_node)
        logger.debug(f"Collected shares: {shares}")
        
        # Update family tree with shares
        logger.debug("Updating family tree with calculated shares...")
        updated_tree = request.family_tree
        update_node_with_shares(updated_tree, shares, estate.total_value)
        
        # Create summary
        logger.debug("Creating inheritance summary...")
        summary = create_inheritance_summary(updated_tree, shares, estate.total_value)
        logger.debug(f"Created summary: {summary}")
        
        response = StructuredInheritanceResponse(
            total_distributed=estate.total_value,
            family_tree=updated_tree,
            summary=summary
        )
        logger.info("Successfully calculated inheritance distribution")
        return response

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during inheritance calculation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while calculating inheritance: {str(e)}"
        )

def convert_schema_to_model(node_schema: FamilyNodeSchema) -> FamilyNode:
    """Convert FamilyNodeSchema to FamilyNode model"""
    try:
        logger.debug(f"Converting node schema: {node_schema}")
        
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
                    try:
                        parent_type = ParentType(parent_type_str.lower())
                        parents[parent_type] = convert_schema_to_model(parent_node)
                    except ValueError:
                        logger.error(f"Invalid parent type: {parent_type_str}")
                        raise HTTPException(
                            status_code=400,
                            detail=f"Invalid parent type: {parent_type_str}. Must be either 'mother' or 'father'"
                        )

        node = FamilyNode(
            person=person,
            spouse=spouse,
            children=children,
            parents=parents
        )
        logger.debug(f"Successfully converted node: {node}")
        return node
        
    except Exception as e:
        logger.error(f"Error converting schema to model: {str(e)}", exc_info=True)
        raise 