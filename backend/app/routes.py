from fastapi import APIRouter, HTTPException
from app.models import Estate
from app.calculations import calculate_inheritance_shares
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/calculate-inheritance")
async def calculate_inheritance(estate: Estate):
    try:
        # Calculate inheritance shares while maintaining family tree structure
        result = calculate_inheritance_shares(estate)
        
        # Log the result before returning
        logger.info("Calculation completed successfully")
        logger.debug(f"Result: {result.dict()}")
        
        return result
    except Exception as e:
        logger.error(f"Error calculating inheritance: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating inheritance: {str(e)}"
        )
