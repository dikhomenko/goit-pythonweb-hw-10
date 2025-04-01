import sys
from pathlib import Path

# Add the 'src' directory to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi import FastAPI
from app.routers import contacts, healthchecks

app = FastAPI()

# Should I extract routes to a separate file?
app.include_router(contacts.router)
app.include_router(healthchecks.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
