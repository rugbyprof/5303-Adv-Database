"""Thin API-key auth.

Right now: compare the ``X-API-Key`` header against a comma-separated ``API_KEYS``
environment variable. If ``API_KEYS`` is unset the API is open (dev mode) and
logs a warning.

Your task (see the assignment README): move keys into a hashed ``api_keys``
table (starter/sql/auth.sql), look the header up by hash, and compare with
``hmac.compare_digest``. Keep the public surface -- ``require_api_key`` -- the
same so the token-auth lecture can swap the body for JWT verification without
touching the routes.
"""

from __future__ import annotations

import hmac
import os
import warnings

from fastapi import Header, HTTPException, status


def _allowed_keys() -> set[str]:
    return {k.strip() for k in os.environ.get("API_KEYS", "").split(",") if k.strip()}


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    """FastAPI dependency. Returns a caller label; raises 401 on a bad key."""
    allowed = _allowed_keys()

    if not allowed:
        warnings.warn("API_KEYS is unset -- auth is disabled (dev mode)", stacklevel=2)
        return "anonymous"

    if x_api_key is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing X-API-Key header")

    # constant-time compare against each configured key
    if not any(hmac.compare_digest(x_api_key, k) for k in allowed):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid X-API-Key")

    return "api-key"
