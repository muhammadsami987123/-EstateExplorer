from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api import properties, locations, search, recommendations, market, reports, saved, ai

app = FastAPI(
    title="AI Real Estate Explorer API",
    version="1.0.0",
    description="Production-grade AI-powered real estate discovery platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/app", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

# Include all routers
app.include_router(properties.router, prefix="/api/properties", tags=["Properties"])
app.include_router(locations.router, prefix="/api/locations", tags=["Locations"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(saved.router, prefix="/api", tags=["Saved & Collections"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])


@app.get("/")
async def root():
    return {
        "message": "AI Real Estate Explorer API",
        "version": "1.0.0",
        "docs": "/docs",
        "frontend": "/app"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
