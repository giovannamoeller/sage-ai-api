from pydantic import BaseModel
from typing import List

class LocationRequest(BaseModel):
  latitude: float
  longitude: float

class RestaurantResponse(BaseModel):
  suggestions: List[str]