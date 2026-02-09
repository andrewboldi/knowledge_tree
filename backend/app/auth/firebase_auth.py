"""Firebase Authentication middleware for FastAPI.

This module provides JWT token verification for Firebase Authentication.
It includes dependency injection functions for protecting API routes.
"""

import os
from typing import Optional

import firebase_admin
from firebase_admin import auth, credentials
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel


class FirebaseUser(BaseModel):
    """Represents an authenticated Firebase user."""

    uid: str
    email: Optional[str] = None
    email_verified: bool = False
    display_name: Optional[str] = None
    photo_url: Optional[str] = None


# Initialize Firebase Admin SDK
_firebase_app: Optional[firebase_admin.App] = None


def _initialize_firebase() -> firebase_admin.App:
    """Initialize Firebase Admin SDK with credentials.

    Looks for credentials in this order:
    1. GOOGLE_APPLICATION_CREDENTIALS environment variable (path to service account JSON)
    2. FIREBASE_SERVICE_ACCOUNT_JSON environment variable (JSON string)
    3. Default credentials (for Cloud Run, GCE, etc.)
    """
    global _firebase_app

    if _firebase_app is not None:
        return _firebase_app

    # Try service account file path
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        _firebase_app = firebase_admin.initialize_app(cred)
        return _firebase_app

    # Try JSON string from environment
    cred_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
    if cred_json:
        import json

        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        _firebase_app = firebase_admin.initialize_app(cred)
        return _firebase_app

    # Fall back to default credentials (Application Default Credentials)
    try:
        _firebase_app = firebase_admin.initialize_app()
        return _firebase_app
    except ValueError:
        # Already initialized
        _firebase_app = firebase_admin.get_app()
        return _firebase_app


# Security scheme for JWT Bearer tokens
security = HTTPBearer(auto_error=False)


async def verify_firebase_token(token: str) -> dict:
    """Verify a Firebase ID token and return the decoded claims.

    Args:
        token: The Firebase ID token to verify.

    Returns:
        The decoded token claims.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    _initialize_firebase()

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> FirebaseUser:
    """FastAPI dependency to get the current authenticated user.

    Use this dependency on routes that require authentication.

    Example:
        @app.get("/protected")
        async def protected_route(user: FirebaseUser = Depends(get_current_user)):
            return {"message": f"Hello {user.email}"}

    Args:
        credentials: The HTTP Authorization header credentials.

    Returns:
        FirebaseUser object with user information.

    Raises:
        HTTPException: If no token is provided or token is invalid.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    decoded = await verify_firebase_token(token)

    return FirebaseUser(
        uid=decoded["uid"],
        email=decoded.get("email"),
        email_verified=decoded.get("email_verified", False),
        display_name=decoded.get("name"),
        photo_url=decoded.get("picture"),
    )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[FirebaseUser]:
    """FastAPI dependency to optionally get the current user.

    Use this dependency on routes where authentication is optional.
    Returns None if no valid token is provided.

    Example:
        @app.get("/public")
        async def public_route(user: Optional[FirebaseUser] = Depends(get_optional_user)):
            if user:
                return {"message": f"Hello {user.email}"}
            return {"message": "Hello anonymous user"}

    Args:
        credentials: The HTTP Authorization header credentials (optional).

    Returns:
        FirebaseUser object if authenticated, None otherwise.
    """
    if credentials is None:
        return None

    try:
        token = credentials.credentials
        decoded = await verify_firebase_token(token)
        return FirebaseUser(
            uid=decoded["uid"],
            email=decoded.get("email"),
            email_verified=decoded.get("email_verified", False),
            display_name=decoded.get("name"),
            photo_url=decoded.get("picture"),
        )
    except HTTPException:
        return None
