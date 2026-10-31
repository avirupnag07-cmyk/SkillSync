"""Authentication, Cryptographic Token Issuance, and Security Dependencies."""

import hashlib
import hmac
import base64
import json
import time
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security_bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Generate secure salted SHA-256 hash for password verification."""
    salt = "skillsync_salt_"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against stored cryptographic hash."""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_in_seconds: Optional[int] = None) -> str:
    """Create a self-contained HMAC-SHA256 JWT string without requiring heavy C extensions."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    now = int(time.time())
    exp = now + (expires_in_seconds or (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60))
    payload["iat"] = now
    payload["exp"] = exp

    def b64_encode(obj: dict) -> str:
        dumped = json.dumps(obj, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(dumped).decode("utf-8").rstrip("=")

    header_b64 = b64_encode(header)
    payload_b64 = b64_encode(payload)
    message = f"{header_b64}.{payload_b64}".encode("utf-8")

    sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), message, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(sig).decode("utf-8").rstrip("=")

    return f"{header_b64}.{payload_b64}.{sig_b64}"


def decode_access_token(token: str) -> Optional[dict]:
    """Validate token signature and expiry, returning decoded payload."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts

        # Verify signature
        message = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), message, hashlib.sha256).digest()
        actual_sig = base64.urlsafe_b64decode(sig_b64 + "==")

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        # Decode payload
        payload_json = base64.urlsafe_b64decode(payload_b64 + "==").decode("utf-8")
        payload = json.loads(payload_json)

        # Check expiry
        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload
    except Exception:
        return None


def get_current_user_optional(auth: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)) -> dict:
    """Extract authenticated user if bearer token is valid, otherwise return a guest identity."""
    if not auth or not auth.credentials:
        return {"sub": "guest_user", "email": "guest@skillsync.io", "is_guest": True}

    payload = decode_access_token(auth.credentials)
    if not payload:
        return {"sub": "guest_user", "email": "guest@skillsync.io", "is_guest": True}

    return {
        "sub": payload.get("sub", "guest_user"),
        "email": payload.get("email", "user@skillsync.io"),
        "is_guest": False
    }


def get_current_user_required(user: dict = Depends(get_current_user_optional)) -> dict:
    """Enforce authenticated non-guest user."""
    if user.get("is_guest", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required for this action."
        )
    return user
