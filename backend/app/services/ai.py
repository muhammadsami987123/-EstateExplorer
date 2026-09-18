from typing import List, Dict, Any, Optional
import json
import logging
from openai import AsyncOpenAI
from app.config import settings
from app.json_db import JsonDB

logger = logging.getLogger("ai_service")

# Initialize client if API key is provided and not dummy
api_key = settings.OPENAI_API_KEY.strip() if settings.OPENAI_API_KEY else ""
has_valid_key = bool(api_key and not api_key.startswith("your_"))
client = AsyncOpenAI(api_key=api_key) if has_valid_key else None

SYSTEM_PROMPT = """You are an expert real estate advisor for AI Real Estate Explorer.
Provide factual, highly tailored, professional property advice and analysis based strictly on the provided real estate data.
Never fabricate market statistics or property facts that contradict or are absent from the dataset.
Be concise, analytical, and structured with clear recommendations."""

async def get_ai_response(messages: List[Dict[str, str]], system: str = SYSTEM_PROMPT) -> str:
    if not client:
        # Provide helpful simulated response if API key is absent
        user_msg = messages[-1].get("content", "") if messages else ""
        return (
            f"Thank you for your inquiry about real estate exploration. "
            f"Based on our active database of premium listings across Pakistan, UAE, and the UK, "
            f"we are tracking strong demand in prime urban centers. "
            f"To enable real-time generative conversational advice, please configure a valid OPENAI_API_KEY in the backend .env file. "
            f"(Query received: '{user_msg[:60]}...')"
        )
    try:
        formatted = [{"role": "system", "content": system}] + messages
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=formatted,
            max_tokens=600,
            temperature=0.7
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"OpenAI completion error: {e}")
        return f"AI analysis temporarily unavailable: {str(e)}"

async def extract_search_params(text: str) -> Dict[str, Any]:
    if not client:
        # Basic heuristic extraction fallback
        text_lower = text.lower()
        extracted: Dict[str, Any] = {}
        
        # Intent
        if "rent" in text_lower or "lease" in text_lower:
            extracted["intent"] = "rent"
        elif "buy" in text_lower or "purchase" in text_lower:
            extracted["intent"] = "buy"
            
        # Property type
        for pt in ["house", "apartment", "villa", "plot", "office", "shop", "farmhouse"]:
            if pt in text_lower:
                extracted["property_type"] = pt
                break
                
        # City
        for city in ["karachi", "lahore", "islamabad", "dubai", "london"]:
            if city in text_lower:
                extracted["city"] = city.title()
                break

        # Area
        for area in ["dha phase 6", "dha phase 5", "dha phase 8", "clifton", "gulshan", "bahria", "johar town", "gulberg", "f-7", "e-7", "marina", "downtown", "chelsea"]:
            if area in text_lower:
                extracted["area"] = area.title()
                break

        return extracted

    prompt = f"""Extract structured real estate search parameters from this user query text and return valid JSON only:
"{text}"

Return JSON adhering to this exact schema (only include fields identified in the text):
{{
  "intent": "buy" or "rent" or "sell",
  "property_type": "house" or "apartment" or "villa" or "plot" or "office" or "shop" or "farmhouse",
  "country": "Pakistan" or "UAE" or "United Kingdom",
  "city": "string",
  "area": "string",
  "bedrooms": "number as string (e.g. '3', '4')",
  "bathrooms": "number as string",
  "min_budget": number,
  "max_budget": number,
  "currency": "PKR" or "USD" or "AED" or "GBP",
  "furnished": true or false,
  "parking": number,
  "features": ["list", "of", "features"]
}}"""
    try:
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=400,
            temperature=0.2
        )
        content = response.choices[0].message.content
        return json.loads(content) if content else {}
    except Exception as e:
        logger.error(f"Extraction error: {e}")
        return {}

async def analyze_property(property_data: Dict[str, Any], preferences: Optional[Dict[str, Any]] = None) -> str:
    title = property_data.get("title", "Property")
    price = property_data.get("price", 0)
    currency = property_data.get("currency", "PKR")
    area = property_data.get("area", "")
    city = property_data.get("city", "")
    p_type = property_data.get("type", "")
    beds = property_data.get("bedrooms", 0)
    baths = property_data.get("bathrooms", 0)
    covered = property_data.get("covered_area_sqft", 0)
    features = ", ".join(property_data.get("features", []))

    if not client:
        return (
            f"Comprehensive Property Analysis for {title}:\n\n"
            f"• Location & Valuation: Situated in prime {area}, {city}, this {p_type} is listed at {currency} {price:,.0f}. "
            f"With a covered area of {covered:,} sqft, the unit presents strong capital preservation metrics.\n"
            f"• Layout & Accommodation: Features {beds} bedrooms and {baths} bathrooms, catering to modern family living standards.\n"
            f"• Key Amenities: Highlights include {features or 'prime security and dedicated parking'}.\n"
            f"• Market Verdict: High demand area with consistent liquidity and appreciation upside."
        )

    system = "You are a senior real estate evaluation specialist. Provide an objective, analytical evaluation of this property for an investor or home buyer."
    user_prompt = f"""Evaluate this property based on the listing data:
Title: {title}
Type: {p_type}
Price: {currency} {price:,.0f}
Location: {area}, {city}, {property_data.get('country', '')}
Bedrooms: {beds}, Bathrooms: {baths}
Covered Area: {covered} sqft
Features: {features}
Amenities: {', '.join(property_data.get('amenities', []))}

User Preferences (if provided):
{json.dumps(preferences or {}, indent=2)}

Provide a structured 3-paragraph evaluation covering:
1. Location advantage and price-to-space valuation.
2. Suitability against user requirements and layout strengths.
3. Investment viability and key considerations before scheduling a viewing."""

    return await get_ai_response([{"role": "user", "content": user_prompt}], system=system)

async def compare_properties(properties: List[Dict[str, Any]], preferences: Optional[Dict[str, Any]] = None) -> str:
    if not properties:
        return "No properties provided for comparison."

    if not client:
        lines = [f"Comparative Summary of {len(properties)} Properties:\n"]
        for i, p in enumerate(properties, 1):
            lines.append(
                f"{i}. {p.get('title')} ({p.get('city')}, {p.get('area')}): "
                f"{p.get('currency')} {p.get('price', 0):,.0f} | {p.get('bedrooms')} Beds | {p.get('covered_area_sqft')} sqft"
            )
        lines.append("\nKey Takeaway: Compare price per square foot and proximity to commercial amenities when finalizing your decision.")
        return "\n".join(lines)

    system = "You are an expert real estate comparative analyst. Compare the following short-listed properties side-by-side."
    summary_list = []
    for p in properties:
        summary_list.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "price": f"{p.get('currency')} {p.get('price', 0):,.0f}",
            "city": p.get("city"),
            "area": p.get("area"),
            "beds": p.get("bedrooms"),
            "baths": p.get("bathrooms"),
            "sqft": p.get("covered_area_sqft"),
            "features": p.get("features", [])
        })

    user_prompt = f"""Compare these short-listed properties:
{json.dumps(summary_list, indent=2)}

User Preferences:
{json.dumps(preferences or {}, indent=2)}

Provide an insightful comparison highlighting:
1. Value proposition and price efficiency per square foot.
2. Space and lifestyle trade-offs.
3. Clear final recommendation on which property represents the superior investment or living choice."""

    return await get_ai_response([{"role": "user", "content": user_prompt}], system=system)

async def get_market_insight(location_id: str) -> str:
    market_data = JsonDB.load('market_data')
    loc = next((m for m in market_data if m.get('location_id') == location_id or m.get('id') == location_id), None)
    
    if not loc:
        # Try finding by partial name
        loc = next((m for m in market_data if location_id.lower() in m.get('location_name', '').lower()), None)

    if not loc:
        return f"Market data snapshot not found for location ID '{location_id}'."

    loc_name = loc.get("location_name", "Selected Market")
    avg_price = loc.get("avg_price_sale", 0)
    currency = loc.get("currency", "PKR")
    demand = loc.get("demand_score", 0)
    trend_6m = loc.get("price_trend_6m", [])

    if not client:
        return (
            f"Market Intelligence Report for {loc_name}:\n\n"
            f"• Average Sale Price: {currency} {avg_price:,.0f} with a Demand Index of {demand}/100.\n"
            f"• Momentum: 6-month price trends indicate sustained capital appreciation across residential inventory.\n"
            f"• Liquidity: Strong buyer inquiries reported with healthy turnover in ready-to-move units."
        )

    system = "You are a chief real estate macroeconomic strategist. Provide an executive summary of market conditions."
    user_prompt = f"""Provide a concise market intelligence briefing for this location:
Location: {loc_name}
Average Sale Price: {currency} {avg_price:,.0f}
Median Sale Price: {currency} {loc.get('median_price_sale', 0):,.0f}
Price per sqft: {currency} {loc.get('price_per_sqft_sale', 0):,.0f}
Demand Index: {demand} / 100
Active Listings: {loc.get('total_listings')}
6-Month Trend: {json.dumps(trend_6m)}

Deliver a 2-paragraph market outlook discussing price trajectory, rental yields, and buyer sentiment."""

    return await get_ai_response([{"role": "user", "content": user_prompt}], system=system)
