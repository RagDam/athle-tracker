"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import auth, rankings, alerts, epreuves, scraping, users
from src.config import settings

# Create FastAPI app
app = FastAPI(
    title="Athle Tracker API",
    description="REST API for athletics rankings tracking",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",  # Next.js dev server (alternate port)
        "http://localhost:3002",  # Next.js dev server (alternate port 2)
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api")
app.include_router(rankings.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(epreuves.router, prefix="/api")
app.include_router(scraping.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.get("/")
def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Athle Tracker API",
        "version": "1.0.0",
        "docs": "/api/docs",
    }


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
