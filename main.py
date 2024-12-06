from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import json
import base64
from io import BytesIO
from PIL import Image
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.chat import (
  ChatPromptTemplate,
  HumanMessagePromptTemplate
)

# Pydantic Models
class CarbBreakdown(BaseModel):
  total: float
  simple: float
  complex: float

class FatBreakdown(BaseModel):
  total: float
  saturated: float
  unsaturated: float

class NutritionalInfo(BaseModel):
  calories: int
  protein: float
  carbs: CarbBreakdown
  fat: FatBreakdown
  fiber: float
  key_nutrients: List[str]

class ScoreBreakdown(BaseModel):
  nutritional_balance: int = Field(..., alias="nutritional_balance")
  portion_size: int = Field(..., alias="portion_size")
  whole_foods: int = Field(..., alias="whole_foods")
  nutrient_density: int = Field(..., alias="nutrient_density")

class HealthScore(BaseModel):
  total: int
  breakdown: ScoreBreakdown

class DietaryInfo(BaseModel):
  allergens: List[str]
  suitable_diets: List[str] = Field(..., alias="suitable_diets")
  glycemic_load: str = Field(..., alias="glycemic_load")

class Suggestions(BaseModel):
  alternatives: List[str]
  modifications: List[str]
  complementary_foods: List[str] = Field(..., alias="complementary_foods")

class PortionAnalysis(BaseModel):
  is_appropriate: bool = Field(..., alias="is_appropriate")
  ideal_portion: str = Field(..., alias="ideal_portion")
  caloric_density: str = Field(..., alias="caloric_density")

class FoodAnalysisResponse(BaseModel):
  nutritional_info: NutritionalInfo
  health_score: HealthScore
  dietary_info: DietaryInfo
  suggestions: Suggestions
  portion_analysis: PortionAnalysis

  class Config:
    populate_by_name = True

# Location Models
class LocationRequest(BaseModel):
  latitude: float
  longitude: float

class RestaurantResponse(BaseModel):
  suggestions: List[str]

class RoutineResponse(BaseModel):
  routine: str

# FastAPI App Setup
app = FastAPI(
  title="SageAI API",
  description="API for food analysis and health recommendations",
  version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# LLM Setup
model_name_groq = "llama-3.1-70b-versatile"
model_name_openai = "gpt-4o-2024-08-06"

llm_openai = ChatOpenAI(
  model=model_name_openai
)

llm_groq = ChatGroq(
  model=model_name_groq
)

parser = PydanticOutputParser(pydantic_object=FoodAnalysisResponse)

async def analyze_with_vision(image_data: str) -> str:
  message=HumanMessage(
    content=[
      {
        "type": "image_url",
        "image_url": {
          "url": f"data:image/jpeg;base64,{image_data}",
            "detail": "low"
        }
      },
      {
        "type": "text",
        "text": "Describe the food items in this image in detail, including visible ingredients, preparation methods, and approximate portions."
      }
    ]
  )
    
  response = llm_openai.invoke([message])
  return response.content

async def analyze_nutrition(food_description: str) -> FoodAnalysisResponse:
  human_prompt = HumanMessagePromptTemplate.from_template("{request}\n{format_instructions}")
  chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
  
  request = chat_prompt.format_prompt(
    request=f"Based on this food description: {food_description}. Provide a detailed nutritional analysis following the exact structure specified. Include realistic values for all nutritional components.",
    format_instructions=parser.get_format_instructions()
  ).to_messages()
  
  results = llm_groq.invoke(request)
  results_values = parser.parse(results.content)
  
  print(f'results_values = {results_values}, {type(results_values)}')
  
  return results_values

@app.post("/analyze_food", response_model=FoodAnalysisResponse)
async def analyze_food(image: UploadFile = File(...)):
  try:
    contents = await image.read()
    img = Image.open(BytesIO(contents))
    img.thumbnail((800, 800))
            
    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=85)
    b64_str = base64.b64encode(buffered.getvalue()).decode()
        
    food_description = await analyze_with_vision(b64_str)
    nutrition_analysis = await analyze_nutrition(food_description)
        
    return nutrition_analysis
  except Exception as e:
    raise HTTPException(
      status_code=500,
      detail=f"Error analyzing food: {str(e)}"
    )

@app.post("/restaurant_suggestions", response_model=RestaurantResponse)
async def get_restaurant_suggestions(location: LocationRequest):
  # Implementation pending
  raise HTTPException(status_code=501, detail="Not implemented")

@app.post("/generate_routine", response_model=RoutineResponse)
async def generate_daily_routine(schedule: dict):
  # Implementation pending
  raise HTTPException(status_code=501, detail="Not implemented")