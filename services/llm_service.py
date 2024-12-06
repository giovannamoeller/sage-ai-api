from langchain_core.messages import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from models.food import FoodAnalysisResponse
from core.llm import get_llm_clients
from langchain.prompts.chat import (
  ChatPromptTemplate,
  HumanMessagePromptTemplate
)

class LLMService:
  def __init__(self):
    self.llm_openai, self.llm_groq = get_llm_clients()
    self.parser = PydanticOutputParser(pydantic_object=FoodAnalysisResponse)

  async def analyze_with_vision(self, image_data: str) -> str:
    message = HumanMessage(
      content=[{
        "type": "image_url",
        "image_url": {
          "url": f"data:image/jpeg;base64,{image_data}",
          "detail": "low"
        }
        }, {
          "type": "text",
          "text": "Describe the food items in this image in detail, including visible ingredients, preparation methods, and approximate portions."
        }]
    )
    response = self.llm_openai.invoke([message])
    return response.content

  async def analyze_nutrition(self, food_description: str) -> FoodAnalysisResponse:
    human_prompt = HumanMessagePromptTemplate.from_template("{request}\n{format_instructions}")
    chat_prompt = ChatPromptTemplate.from_messages([human_prompt])
  
    request = chat_prompt.format_prompt(
      request=f"Based on this food description: {food_description}. Provide a detailed nutritional analysis following the exact structure specified. Include realistic values for all nutritional components.",
      format_instructions=self.parser.get_format_instructions()
    ).to_messages()
  
    results = self.llm_groq.invoke(request)
    results_values = self.parser.parse(results.content)
        
    return results_values