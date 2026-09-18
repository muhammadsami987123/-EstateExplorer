from pydantic import BaseModel
from typing import Optional, List, Any, Dict

class SearchPreferences(BaseModel):
    intent: Optional[str] = None  # buy, rent, sell
    purpose: Optional[str] = None  # personal, investment, both
    property_type: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    min_budget: Optional[float] = None
    max_budget: Optional[float] = None
    currency: str = "PKR"
    bedrooms: Optional[str] = None  # "1", "2", "3", "4", "5", "6+", "Studio", "Flexible"
    bathrooms: Optional[str] = None
    parking: Optional[int] = None
    furnished: Optional[bool] = None
    features: Optional[List[str]] = []
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    session_id: Optional[str] = None

class SearchSessionCreate(BaseModel):
    name: str
    preferences: SearchPreferences
    session_id: Optional[str] = None

class SearchSessionItem(BaseModel):
    id: str
    name: str
    preferences: Dict[str, Any]
    session_id: Optional[str] = None
    created_at: str

class SearchResultGroups(BaseModel):
    recommended: List[Dict[str, Any]]
    strong_matches: List[Dict[str, Any]]
    budget_friendly: List[Dict[str, Any]]
    premium: List[Dict[str, Any]]
    nearby: List[Dict[str, Any]]
    total_matches: int
