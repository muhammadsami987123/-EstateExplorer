from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.schemas.search import SearchPreferences

class ReportGenerateRequest(BaseModel):
    preferences: SearchPreferences

class ReportResponse(BaseModel):
    id: str
    created_at: str
    preferences: Dict[str, Any]
    recommended_properties: List[Dict[str, Any]]
    alternative_properties: List[Dict[str, Any]]
    market_snapshot: Optional[Dict[str, Any]] = None
    total_matches: int
    data_type: str = "Demo Dataset"
    next_steps: List[str]
    disclaimer: str
