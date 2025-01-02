from fastapi import APIRouter
from app.models import Estate
from app.calculations import calculate_inheritance_shares

router = APIRouter()

@router.post("/calculate-inheritance")
def calculate_inheritance(estate: Estate):
    result = calculate_inheritance_shares(estate)
    return result
