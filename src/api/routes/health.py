"""Health check endpoints."""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Student Performance Analyzer"
    }


@router.get("/info")
def api_info():
    """API information endpoint."""
    return {
        "name": "AI Student Performance Analyzer API",
        "version": "1.0.0",
        "description": "ML-powered student performance prediction and recommendations",
        "endpoints": {
            "predictions": "/api/v1/predictions",
            "models": "/api/v1/models",
            "health": "/api/v1/health"
        }
    }
