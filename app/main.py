#     # app/main.py
from fastapi import FastAPI
from app.properties.routers import router as properties_router

app = FastAPI()

# Include routers
app.include_router(properties_router)