from typing import Dict, Any, List
from app.json_db import JsonDB
from app.services.matching import score_property

def get_recommendations(preferences: Dict[str, Any]) -> Dict[str, Any]:
    all_properties = JsonDB.load('properties')
    active_properties = [p for p in all_properties if p.get('status', 'active') == 'active']
    
    # Filter by intent / listing_type
    intent = preferences.get('intent', '').lower().strip()
    target_listing_type = 'rent' if intent == 'rent' else 'sale'
    
    candidates = [p for p in active_properties if p.get('listing_type') == target_listing_type]
    if not candidates:
        candidates = active_properties
    
    # Filter by country or city if provided
    country = preferences.get('country')
    if country:
        country_matches = [p for p in candidates if p.get('country', '').lower() == country.lower()]
        if country_matches:
            candidates = country_matches

    # Score every candidate
    scored = []
    for prop in candidates:
        match_info = score_property(prop, preferences)
        enriched = {
            **prop,
            'match_score': match_info['score'],
            'match_data': match_info
        }
        scored.append(enriched)
        
    scored.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Categorize into groups
    # 1. Recommended: top matches
    recommended = scored[:6]
    
    # 2. Strong Matches: score >= 65, next batch
    strong_matches = [p for p in scored[6:] if p['match_score'] >= 60][:6]
    if not strong_matches and len(scored) > 6:
        strong_matches = scored[6:12]
        
    # 3. Budget Friendly: price <= 85% of max_budget (if set) or lowest price half
    max_budget = preferences.get('max_budget')
    if max_budget and max_budget > 0:
        budget_friendly = [p for p in scored if p.get('price', 0) <= max_budget * 0.85]
    else:
        # Sort by price ascending
        budget_friendly = sorted(scored, key=lambda x: x.get('price', 0))
    budget_friendly = budget_friendly[:4]
    
    # 4. Premium: luxury tier / featured or highest price
    premium = sorted(
        [p for p in scored if p.get('featured') or p.get('price', 0) >= (max_budget or 50000000)],
        key=lambda x: x.get('price', 0),
        reverse=True
    )[:4]
    if not premium:
        premium = sorted(scored, key=lambda x: x.get('price', 0), reverse=True)[:4]

    # 5. Nearby / Alternative areas in the same city or region
    pref_city = (preferences.get('city') or '').lower()
    pref_area = (preferences.get('area') or '').lower()
    if pref_city:
        nearby = [
            p for p in scored
            if p.get('city', '').lower() == pref_city and p.get('area', '').lower() != pref_area
        ][:4]
    else:
        nearby = scored[12:16]

    total_valid = len([p for p in scored if p['match_score'] >= 50]) or len(scored)

    return {
        'recommended': recommended,
        'strong_matches': strong_matches,
        'budget_friendly': budget_friendly,
        'premium': premium,
        'nearby': nearby,
        'total_matches': total_valid
    }
