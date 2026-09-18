from typing import Optional, List, Dict, Any
from app.json_db import JsonDB

def get_all_market_data() -> List[Dict[str, Any]]:
    return JsonDB.load('market_data')

def get_market_stats(location_id: str) -> Optional[Dict[str, Any]]:
    market_data = JsonDB.load('market_data')
    # Direct match by location_id
    found = next((m for m in market_data if m.get('location_id') == location_id), None)
    if found:
        return found
    
    # Fallback match by id (e.g. MKT-001)
    found = next((m for m in market_data if m.get('id') == location_id), None)
    if found:
        return found
    
    # Fallback match by partial location name or city
    loc_lower = location_id.lower().replace('-', ' ')
    found = next((m for m in market_data if loc_lower in m.get('location_name', '').lower() or loc_lower in m.get('city', '').lower()), None)
    return found
