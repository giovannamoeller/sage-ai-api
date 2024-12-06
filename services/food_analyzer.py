from .image_processor import ImageProcessor
from .llm_service import LLMService
from models.food import FoodAnalysisResponse

class FoodAnalyzer:
  def __init__(self):
    self.image_processor = ImageProcessor()
    self.llm_service = LLMService()

  async def analyze(self, image_data: bytes) -> FoodAnalysisResponse:
    processed_image = await self.image_processor.process_image(image_data)
    food_description = await self.llm_service.analyze_with_vision(processed_image)
    nutrition_analysis = await self.llm_service.analyze_nutrition(food_description)
    return nutrition_analysis