from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.json_db import JsonDB

router = APIRouter()

@router.get("")
async def list_properties(
    city: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    listing_type: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    bedrooms: Optional[int] = Query(None),
    bathrooms: Optional[int] = Query(None),
    furnished: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    sort_by: str = Query("listed_date"),
    sort_order: str = Query("desc")
):
    properties = JsonDB.load('properties')
    
    # Apply filters
    if city:
        properties = [p for p in properties if p.get('city', '').lower() == city.lower().strip()]
    if area:
        properties = [p for p in properties if area.lower().strip() in p.get('area', '').lower()]
    if country:
        properties = [p for p in properties if p.get('country', '').lower() == country.lower().strip()]
    if type:
        properties = [p for p in properties if p.get('type', '').lower() == type.lower().strip()]
    if listing_type:
        properties = [p for p in properties if p.get('listing_type', '').lower() == listing_type.lower().strip()]
    if min_price is not None:
        properties = [p for p in properties if p.get('price', 0) >= min_price]
    if max_price is not None:
        properties = [p for p in properties if p.get('price', 0) <= max_price]
    if bedrooms is not None:
        properties = [p for p in properties if p.get('bedrooms') == bedrooms]
    if bathrooms is not None:
        properties = [p for p in properties if p.get('bathrooms') == bathrooms]
    if furnished is not None:
        properties = [p for p in properties if p.get('furnished') == furnished]
        
    properties = [p for p in properties if p.get('status', 'active') == 'active']

    # Sort
    reverse = (sort_order.lower() == "desc")
    if sort_by == "price":
        properties.sort(key=lambda x: x.get('price', 0), reverse=reverse)
    elif sort_by == "area":
        properties.sort(key=lambda x: x.get('covered_area_sqft', 0), reverse=reverse)
    else:
        properties.sort(key=lambda x: x.get('listed_date', ''), reverse=reverse)

    # Paginate
    total = len(properties)
    start = (page - 1) * limit
    end = start + limit
    total_pages = (total + limit - 1) // limit if total > 0 else 1

    return {
        "properties": properties[start:end],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": total_pages
    }

@router.get("/featured")
async def featured_properties():
    props = JsonDB.load('properties')
    featured = [p for p in props if p.get('featured') and p.get('status') == 'active']
    return {"properties": featured[:6]}

@router.get("/{property_id}")
async def get_property(property_id: str):
    prop = JsonDB.find_one('properties', property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop
