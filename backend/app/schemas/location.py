from pydantic import BaseModel
from typing import Optional, List

class LocationItem(BaseModel):
    id: str
    name: str
    type: str  # country, region, city, area, neighborhood
    parent_id: Optional[str] = None
    currency: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    property_count: Optional[int] = None

class LocationListResponse(BaseModel):
    locations: List[LocationItem]
