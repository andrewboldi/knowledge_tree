"""Firebase Authentication integration."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


async def verify_firebase_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify Firebase JWT token and return user info."""
    raise NotImplementedError("Firebase auth verification not yet implemented")


async def get_current_user(token_data: dict = Depends(verify_firebase_token)) -> dict:
    """Get current authenticated user."""
    return token_data
