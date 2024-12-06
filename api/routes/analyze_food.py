from fastapi import APIRouter, File, UploadFile, HTTPException
from services.food_analyzer import FoodAnalyzer
from models.food import FoodAnalysisResponse

router = APIRouter()
food_analyzer = FoodAnalyzer()

@router.post("/analyze_food", response_model=FoodAnalysisResponse)
async def analyze_food(image: UploadFile = File(...)):
  try:
      contents = await image.read()
      return await food_analyzer.analyze(contents)
  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail=f"Error analyzing food: {str(e)}"
    )