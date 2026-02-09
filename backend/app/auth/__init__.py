"""Firebase authentication module for FastAPI."""

from .firebase_auth import (
    verify_firebase_token,
    get_current_user,
    get_optional_user,
    FirebaseUser,
)

__all__ = [
    "verify_firebase_token",
    "get_current_user",
    "get_optional_user",
    "FirebaseUser",
]
