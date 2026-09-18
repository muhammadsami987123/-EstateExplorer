from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TrendItem(BaseModel):
    month: str
    value: float

class MarketSnapshot(BaseModel):
    id: str
    location_id: str
    location_name: str
    city: str
    avg_price_sale: float
    median_price_sale: float
    min_price_sale: float
    max_price_sale: float
    avg_price_rent_monthly: float
    price_per_sqft_sale: float
    price_per_sqft_rent: float
    total_listings: int
    sale_listings: int
    rent_listings: int
    property_distribution: Dict[str, Any]
    price_trend_6m: List[TrendItem]
    price_trend_1y: List[TrendItem]
    price_trend_3y: List[TrendItem]
    demand_score: int
    data_type: str = "Demo Dataset"
    data_source: str
    last_updated: str
    currency: str = "PKR"
