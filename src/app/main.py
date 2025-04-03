import sys
from pathlib import Path

# Add the 'src' directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.routers.contacts import contacts
from fastapi import FastAPI, status, Request
from app.routers import healthchecks
from app.routers.users import users
from app.routers.auth import auth
from app.helpers.api.rate_limiter import limiter, rate_limit_exception_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware

# Init fastapi app
app = FastAPI()

app.state.limiter = limiter

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

# Add the rate limit exception handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)

origins = [
    "<http://localhost:3000>",
    "<http://127.0.0.1/8000>",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router)
app.include_router(healthchecks.router)
app.include_router(users.router)
app.include_router(auth.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
