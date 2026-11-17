"""Entrypoint for the HF Space: runs OpenPronounce server with optional API-key auth."""
import os

import uvicorn

from fastapi import Depends, Header, HTTPException
from fastapi.responses import JSONResponse

import server  # the upstream server module

EXPECTED_KEY = os.environ.get("OPENPRONOUNCE_API_KEY", "").strip()


def require_key(x_api_key: str = Header(default="")):
    if EXPECTED_KEY and x_api_key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="invalid or missing X-Api-Key")


# Wrap the upstream /pronunciation route with auth if a key is configured.
if EXPECTED_KEY:
    # Re-register with dependency by overriding: FastAPI routes are immutable,
    # so instead we monkey-patch via a middleware that checks the header on
    # /pronunciation only.
    from starlette.middleware.base import BaseHTTPMiddleware

    class ApiKeyMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            if request.url.path == "/pronunciation" and EXPECTED_KEY:
                key = request.headers.get("x-api-key", "")
                if key != EXPECTED_KEY:
                    return JSONResponse({"detail": "invalid or missing X-Api-Key"}, status_code=401)
            return await call_next(request)

    server.app.add_middleware(ApiKeyMiddleware)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(server.app, host="0.0.0.0", port=port, log_level="info")
