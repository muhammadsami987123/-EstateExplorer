from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.json_db import JsonDB

router = APIRouter()

@router.get("/countries")
async def get_countries():
    locs = JsonDB.load('locations')
    return [l for l in locs if l.get('type') == 'country']

@router.get("/search")
async def search_locations(q: str = Query(..., min_length=1)):
    locs = JsonDB.load('locations')
    q_lower = q.lower().strip()
    return [l for l in locs if q_lower in l.get('name', '').lower()][:10]

@router.get("/{location_id}/children")
async def get_children(location_id: str):
    locs = JsonDB.load('locations')
    children = [l for l in locs if l.get('parent_id') == location_id]
    return children

@router.get("/{location_id}")
async def get_location(location_id: str):
    locs = JsonDB.load('locations')
    loc = next((l for l in locs if l.get('id') == location_id), None)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return loc

@router.get("")
async def list_locations():
    return JsonDB.load('locations')
