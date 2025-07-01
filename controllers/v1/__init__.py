"""API v1 router configuration.

This module sets up the main API router and includes all sub-routers for different
endpoints like authentication and chatbot functionality.
"""


import logging
from fastapi import APIRouter
from .chatbot import router as chatbot_router

logger = logging.getLogger(__name__)

api_router = APIRouter()

# include routers
api_router.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])

@api_router.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        dict: Health status information.
    """

    logger.info("health_check_called")
    return {
        "status": "healthy",
        "version": "1.0.0"    
    }