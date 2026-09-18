from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from app.schemas.search import SearchPreferences, SearchSessionCreate
from app.services.recommendations import get_recommendations
from app.json_db import JsonDB

router = APIRouter()

@router.post("")
async def search_properties(preferences: SearchPreferences):
    pref_dict = preferences.model_dump()
    results = get_recommendations(pref_dict)
    return results

@router.get("/sessions")
async def list_search_sessions(session_id: Optional[str] = Query(None)):
    sessions = JsonDB.load('search_sessions')
    if session_id:
        sessions = [s for s in sessions if s.get('session_id') == session_id]
    return sessions

@router.post("/sessions")
async def save_search_session(payload: SearchSessionCreate):
    session_data = {
        "id": str(uuid.uuid4()),
        "name": payload.name,
        "preferences": payload.preferences.model_dump(),
        "session_id": payload.session_id,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    saved = JsonDB.insert('search_sessions', session_data)
    return saved

@router.delete("/sessions/{session_id}")
async def delete_search_session(session_id: str):
    success = JsonDB.delete('search_sessions', session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Search session not found")
    return {"success": True, "message": "Search session removed"}
