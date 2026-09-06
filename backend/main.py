from fastapi import FastAPI
from backend.routes.generate import router

app = FastAPI()

app.include_router(router, prefix="/api", tags=["generate"])
