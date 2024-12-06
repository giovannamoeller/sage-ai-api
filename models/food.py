from pydantic import BaseModel, Field
from typing import List

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