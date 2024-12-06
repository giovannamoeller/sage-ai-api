from fastapi import APIRouter, HTTPException
from models.location import LocationRequest, RestaurantResponse

router = APIRouter()

@router.post("/restaurant_suggestions", response_model=RestaurantResponse)
async def get_restaurant_suggestions(location: LocationRequest):
  raise HTTPException(status_code=501, detail="Not implemented")