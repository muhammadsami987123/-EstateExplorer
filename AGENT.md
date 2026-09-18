# AGENT.md — Multi-Agent Build Architecture

This project was built using a parallel multi-agent development approach.

## Agent Responsibilities
| Agent | Files Built |
|---|---|
| Backend Core | FastAPI app, JSON DB, all API routes, services, 60 data entries |
| Frontend & Docs | All HTML pages, CSS design system, JS utilities, documentation |

## Architecture Decisions
### JSON Database
Using JSON files instead of SQLite/PostgreSQL for zero-dependency simplicity.
Threading locks ensure concurrent request safety.
Easy to inspect, modify, and reset data.

### Vanilla JS
No framework overhead. ES Modules for code organization.
Faster initial load, simpler architecture.

### AI Separation
Backend handles all calculations (matching, filtering, sorting).
AI (OpenAI) only handles natural language: explanations, extraction, summaries.
