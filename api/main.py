from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from .routes import analyze_food, get_restaurants, create_routine

app = FastAPI(
  title=settings.app_name,
  description=settings.app_description,
  version=settings.app_version
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(analyze_food.router, tags=["Food Analysis"])
app.include_router(get_restaurants.router, tags=["Restaurant Suggestions"])
app.include_router(create_routine.router, tags=["Daily Routine"])