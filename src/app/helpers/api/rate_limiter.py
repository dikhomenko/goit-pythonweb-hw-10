from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import Request
from starlette.responses import JSONResponse
from starlette import status

limiter = Limiter(key_func=get_remote_address)


def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    print(f"Client IP: {request.client.host}")
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Resource limit exceeded", "message": str(exc.detail)},
    )
