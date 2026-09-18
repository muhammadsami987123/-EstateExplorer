from fastapi import APIRouter, HTTPException
from app.services.market import get_all_market_data, get_market_stats

router = APIRouter()


@router.get("")
async def list_market_data():
    """Return all market data snapshots."""
    return get_all_market_data()


@router.get("/{location_id}")
async def get_market_data(location_id: str):
    """Get market stats for a specific location."""
    data = get_market_stats(location_id)
    if not data:
        raise HTTPException(status_code=404, detail="Market data not found for this location")
    return data
