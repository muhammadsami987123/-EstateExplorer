from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from datetime import datetime
import uuid

from app.json_db import JsonDB

router = APIRouter()


# ── Saved Properties ──────────────────────────────────────────────

@router.get("/saved")
async def list_saved(x_session_id: Optional[str] = Header(None, alias="X-Session-ID")):
    """List saved properties for the current session."""
    saved = JsonDB.load('saved_properties')
    if x_session_id:
        saved = [s for s in saved if s.get('session_id') == x_session_id]
    return {"saved": saved, "total": len(saved)}


@router.post("/saved")
async def save_property(
    payload: dict,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Save/bookmark a property. Frontend sends { property_id }."""
    property_id = payload.get("property_id")
    if not property_id:
        raise HTTPException(status_code=400, detail="property_id is required")

    # Prevent duplicates within the same session
    saved = JsonDB.load('saved_properties')
    existing = next(
        (s for s in saved if s.get('property_id') == property_id and s.get('session_id') == x_session_id),
        None
    )
    if existing:
        return existing

    # Attach full property data for offline display
    prop = JsonDB.find_one('properties', property_id)

    item = {
        "id": str(uuid.uuid4()),
        "property_id": property_id,
        "session_id": x_session_id,
        "property": prop,
        "notes": payload.get("notes", ""),
        "collection_id": payload.get("collection_id"),
        "saved_at": datetime.utcnow().isoformat() + "Z"
    }
    result = JsonDB.insert('saved_properties', item)
    return result


@router.delete("/saved/{property_id}")
async def unsave_property(
    property_id: str,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Remove a saved property. Matches by property_id or saved item id."""
    saved = JsonDB.load('saved_properties')
    target = next(
        (s for s in saved
         if (s.get('property_id') == property_id or s.get('id') == property_id)
         and (not x_session_id or s.get('session_id') == x_session_id)),
        None
    )
    if not target:
        raise HTTPException(status_code=404, detail="Saved property not found")
    JsonDB.delete('saved_properties', target['id'])
    return {"success": True, "message": "Property removed from saved"}


# ── Collections ───────────────────────────────────────────────────

@router.get("/collections")
async def list_collections(x_session_id: Optional[str] = Header(None, alias="X-Session-ID")):
    """List all collections for the current session."""
    collections = JsonDB.load('collections')
    if x_session_id:
        collections = [c for c in collections if c.get('session_id') == x_session_id]
    return {"collections": collections, "total": len(collections)}


@router.post("/collections")
async def create_collection(
    payload: dict,
    x_session_id: Optional[str] = Header(None, alias="X-Session-ID")
):
    """Create a new collection."""
    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Collection name is required")

    collection = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": payload.get("description", ""),
        "session_id": x_session_id,
        "property_ids": [],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    result = JsonDB.insert('collections', collection)
    return result


@router.post("/collections/{collection_id}/properties")
async def add_property_to_collection(collection_id: str, payload: dict):
    """Add a property to a collection. Frontend sends { property_id }."""
    property_id = payload.get("property_id")
    if not property_id:
        raise HTTPException(status_code=400, detail="property_id is required")

    collection = JsonDB.find_one('collections', collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    prop_ids = collection.get("property_ids", [])
    if property_id not in prop_ids:
        prop_ids.append(property_id)
        JsonDB.update('collections', collection_id, {"property_ids": prop_ids})

    return {"success": True, "message": "Property added to collection"}


@router.delete("/collections/{collection_id}")
async def delete_collection(collection_id: str):
    """Delete a collection by ID."""
    success = JsonDB.delete('collections', collection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Collection not found")
    return {"success": True, "message": "Collection deleted"}
