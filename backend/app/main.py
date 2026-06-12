from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, health
from app.models.user import User
from app.models.facebook import FacebookPage

# Create tables for dev
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoPoster API")

# Set up CORS
origins = []
if settings.FRONTEND_URL:
    origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-New-Token"],
)

app.include_router(health.router)
app.include_router(auth.router)
from app.routers import facebook
app.include_router(facebook.router)
