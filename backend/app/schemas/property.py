from pydantic import BaseModel, Field
from typing import Optional, List, Any

class PropertyItem(BaseModel):
    id: str
    type: str
    purpose: str
    listing_type: str
    title: str
    description: str
    country: str
    region: str
    city: str
    area: str
    neighborhood: Optional[str] = ""
    address: str
    lat: float
    lng: float
    price: float
    currency: str
    price_per_sqft: Optional[float] = None
    bedrooms: Optional[int] = 0
    bathrooms: Optional[int] = 0
    parking: Optional[int] = 0
    covered_area_sqft: Optional[float] = 0
    plot_size_sqft: Optional[float] = 0
    floors: Optional[int] = 1
    furnished: Optional[bool] = False
    condition: Optional[str] = "good"
    age_years: Optional[int] = 0
    gated_community: Optional[bool] = False
    features: List[str] = []
    amenities: List[str] = []
    images: List[str] = []
    data_source: str = "Demo Dataset"
    listed_date: str
    status: str = "active"
    featured: bool = False
    location_id: Optional[str] = None
    match_score: Optional[int] = None
    match_data: Optional[dict] = None

class PropertyFilter(BaseModel):
    city: Optional[str] = None
    area: Optional[str] = None
    country: Optional[str] = None
    type: Optional[str] = None
    listing_type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    currency: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    furnished: Optional[bool] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    features: Optional[List[str]] = None
    page: int = 1
    limit: int = 12
    sort_by: str = "listed_date"
    sort_order: str = "desc"

class PropertyListResponse(BaseModel):
    properties: List[PropertyItem]
    total: int
    page: int
    limit: int
    pages: int

class PropertyFeaturedResponse(BaseModel):
    properties: List[PropertyItem]
