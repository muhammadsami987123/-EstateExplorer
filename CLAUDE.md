# CLAUDE.md — AI Real Estate Explorer

## Project Overview
Production-grade AI-powered real estate discovery platform.

## Stack
- Backend: Python 3.11 + FastAPI + JSON file database (NO ORM)
- Frontend: Vanilla JS ES Modules + Custom CSS (NO React/Next.js)
- AI: OpenAI GPT-4o-mini (abstracted, Gemini also supported)
- Maps: MapLibre GL JS + OpenStreetMap tiles
- Charts: Chart.js

## Critical Rules
1. NEVER use SQLAlchemy — JSON file DB only (json_db.py)
2. NEVER use React/Next.js — Vanilla JS only
3. All market data must be labeled [Demo Dataset]
4. AI must only use data provided in request context
5. All API endpoints use Pydantic v2 validation
6. Frontend JS uses ES modules (type="module")
7. Dark mode via [data-theme="dark"] on <html>
8. Session ID stored in localStorage as 'session_id'

## Data Files Location
All data in `backend/app/data/*.json`
CRUD via `JsonDB` class in `backend/app/json_db.py`

## Running
```bash
cd backend && python run.py
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## Design System
CSS variables defined in `frontend/css/main.css`
Primary accent: #C9A96E (gold)
Heading font: Playfair Display
Body font: Inter
