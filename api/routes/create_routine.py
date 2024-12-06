from fastapi import APIRouter, HTTPException
from models.routine import RoutineResponse

router = APIRouter()

@router.post("/generate_routine", response_model=RoutineResponse)
async def generate_daily_routine(schedule: dict):
  raise HTTPException(status_code=501, detail="Not implemented")