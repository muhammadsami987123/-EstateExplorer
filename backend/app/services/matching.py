from typing import Dict, Any, List

def score_property(property: Dict[str, Any], preferences: Dict[str, Any]) -> Dict[str, Any]:
    score = 0
    breakdown = {}
    positives = []
    compromises = []

    # 1. Budget (30 points)
    price = property.get('price', 0)
    max_budget = preferences.get('max_budget')
    if max_budget and max_budget > 0:
        if price <= max_budget:
            budget_score = 30
            positives.append('Within your budget')
        elif price <= max_budget * 1.05:
            budget_score = 22
            compromises.append(f'Slightly above budget ({round((price/max_budget-1)*100)}%)')
        elif price <= max_budget * 1.10:
            budget_score = 15
            compromises.append(f'Above budget ({round((price/max_budget-1)*100)}%)')
        elif price <= max_budget * 1.20:
            budget_score = 8
            compromises.append(f'Significantly above budget ({round((price/max_budget-1)*100)}%)')
        else:
            budget_score = 0
            compromises.append('Well above budget')
        score += budget_score
        breakdown['budget'] = {'score': budget_score, 'max': 30}
    else:
        budget_score = 30
        score += budget_score
        breakdown['budget'] = {'score': budget_score, 'max': 30}

    # 2. Location (25 points)
    pref_area = preferences.get('area', '').lower().strip() if preferences.get('area') else ''
    pref_city = preferences.get('city', '').lower().strip() if preferences.get('city') else ''
    prop_area = property.get('area', '').lower().strip()
    prop_city = property.get('city', '').lower().strip()

    if pref_area and (pref_area in prop_area or prop_area in pref_area):
        loc_score = 25
        positives.append(f"In preferred area ({property.get('area')})")
    elif pref_city and (pref_city in prop_city or prop_city in pref_city):
        loc_score = 15
        compromises.append('In preferred city but different area')
    elif not pref_city and not pref_area:
        loc_score = 20
    else:
        loc_score = 0
    score += loc_score
    breakdown['location'] = {'score': loc_score, 'max': 25}

    # 3. Property type (20 points)
    pref_type = preferences.get('property_type', '').lower().strip() if preferences.get('property_type') else ''
    prop_type = property.get('type', '').lower().strip()
    if pref_type:
        if pref_type == prop_type:
            type_score = 20
            positives.append(f"Exact type match ({property.get('type', '').title()})")
        else:
            type_score = 0
    else:
        type_score = 20
    score += type_score
    breakdown['type'] = {'score': type_score, 'max': 20}

    # 4. Bedrooms (10 points)
    pref_beds = preferences.get('bedrooms')
    prop_beds = property.get('bedrooms', 0)
    if pref_beds and str(pref_beds) not in ['Flexible', 'Studio', '']:
        try:
            req_beds = int(str(pref_beds).replace('+', '').strip())
            if prop_beds == req_beds:
                bed_score = 10
                positives.append(f'{prop_beds} bedrooms as requested')
            elif abs(prop_beds - req_beds) == 1:
                bed_score = 7
                compromises.append(f'{prop_beds} beds (requested {req_beds})')
            elif abs(prop_beds - req_beds) == 2:
                bed_score = 3
                compromises.append(f'{prop_beds} beds (requested {req_beds})')
            else:
                bed_score = 0
        except Exception:
            bed_score = 5
    else:
        bed_score = 10 if prop_beds > 0 or prop_type in ['plot', 'office', 'shop'] else 5
    score += bed_score
    breakdown['bedrooms'] = {'score': bed_score, 'max': 10}

    # 5. Features (10 points)
    pref_features = preferences.get('features') or []
    prop_features = property.get('features') or []
    if pref_features:
        matched = sum(1 for f in pref_features if f.lower() in [x.lower() for x in prop_features])
        feat_score = int((matched / len(pref_features)) * 10)
        if feat_score >= 8:
            positives.append('Most requested features present')
        elif feat_score < 5:
            missing = [f for f in pref_features if f.lower() not in [x.lower() for x in prop_features]]
            if missing:
                compromises.append(f"Missing: {', '.join(missing[:2])}")
    else:
        feat_score = 7
    score += feat_score
    breakdown['features'] = {'score': feat_score, 'max': 10}

    # 6. Bathrooms (5 points)
    pref_baths = preferences.get('bathrooms')
    prop_baths = property.get('bathrooms', 0)
    if not pref_baths or str(pref_baths) in ['Flexible', 'Studio', '']:
        bath_score = 5
    else:
        try:
            req_baths = int(str(pref_baths).replace('+', '').strip())
            bath_score = 5 if prop_baths >= req_baths else 2
        except Exception:
            bath_score = 5
    score += bath_score
    breakdown['bathrooms'] = {'score': bath_score, 'max': 5}

    grade = (
        'Perfect Match' if score >= 90 else
        'Strong Match' if score >= 75 else
        'Good Match' if score >= 60 else
        'Partial Match' if score >= 40 else
        'Low Match'
    )

    return {
        'score': min(score, 100),
        'grade': grade,
        'breakdown': breakdown,
        'positives': positives,
        'compromises': compromises
    }
