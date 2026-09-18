# GEMINI.md — AI Real Estate Explorer

## Developer
Muhammad Sami Asghar Mughal — AI Agent Engineer & Full-Stack Developer

## Architecture Rules
- Backend: FastAPI + JSON files (no SQLAlchemy)
- Frontend: Vanilla JS ES Modules (no frameworks)
- AI: OpenAI default, Gemini supported via env var
- Follow existing CSS design system
- Pydantic v2 for all schemas

## Key Patterns
- API client: frontend/js/api.js (api.get/post/delete)
- DB operations: backend/app/json_db.py (JsonDB class)
- Session: localStorage 'session_id' → passed as X-Session-ID header
