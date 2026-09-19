from contextlib import asynccontextmanager

import httpx
from fastapi import Depends, FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=10.0)
    app.state.db = {}
    app.state.jobs = {}
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

# Dependencies

def get_db(request: Request) -> dict:
    return request.app.state.db

def get_jobs(request: Request) -> dict:
    return request.app.state.jobs

async def get_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/readyz")
async def readyz(client: httpx.AsyncClient = Depends(get_client)):
    return {"status": "ready", "client_status": not client.is_closed}