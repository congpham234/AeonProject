from fastapi import FastAPI
from app.api import ping

app = FastAPI()

# Include routers
app.include_router(ping.router)