# controllers/test_router.py

from fastapi import APIRouter, Request
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/test")
async def test_endpoint(request: Request):
    logger.info("test_endpoint called")

    engine = getattr(request.app.state, "engine", None)
    logger.info(f"Retrieved engine: {engine}")

    return {
        "message": "Test endpoint is working!",
        "engine_repr": str(engine)
    }
