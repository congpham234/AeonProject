from fastapi import FastAPI
from app.api import ping
from app.api import llama

app = FastAPI()

# Include routers
app.include_router(ping.router)
app.include_router(llama.router)
