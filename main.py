"""Main entry point for FastAPI application."""
import uvicorn
from src.api.main import create_app
from src.core.config import config

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.API_RELOAD
    )
