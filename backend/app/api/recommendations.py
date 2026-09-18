from fastapi import APIRouter
from app.schemas.search import SearchPreferences
from app.services.recommendations import get_recommendations

router = APIRouter()


@router.post("")
async def recommend(preferences: SearchPreferences):
    """Get AI-scored property recommendations based on user preferences."""
    pref_dict = preferences.model_dump()
    results = get_recommendations(pref_dict)
    return results
