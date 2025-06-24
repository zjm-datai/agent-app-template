"""Authentication and authorization endpoint for the API.

This module provides endpoint for user registeration, login, session management,
and token verfication.
"""

import uuid 
from typing import List 

from fastapi import (
    APIRouter,
    Depends, 
    Form, 
    HTTPException    
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials 
)

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)        
) -> User:
    """Get the current user ID from the token.
    
    Args:
        credentials: The HTTP authorization credentials containing the JWT token.

    Returns:
        User: The user extracted from the token.

    Raise:
        HTTPException: If the token is invalid or missing.
    """

    try:
        # Sanitize token 
        token = sanitize_string(credentials.credentials)

        user_id = verify_token(token)
        if user_id is None:
            logger.error("invalid_token", token_part=token[:10] + "...")
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},  
            )
        

@router.post("/login", response_model=TokenResponse)
@limier.limit(config.RATE_LIMIT_ENDPOINTS["login"][0])
async def login(
    request: Request, username: str = Form(...), password: str = Form(...), grant_type: str = Form(default="password")    
):
    """Login a user
    
    Args:
        request: The FastAPI request object for rate limiting.
        username: User's email
        password: User's password
        grant_type: Must be "password"

    Returns:
        TokenResponse: Access token information

    Raises:
        HTTPException: If credentials are invalid
    """

    try:
        # Sanitize inputs
        username = sanitize_string(username)
        password = sanitize_string(password)
        grant_type = sanitize_string(grant_type)

        