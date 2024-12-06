from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from .config import settings

def get_llm_clients():
  llm_openai = ChatOpenAI(model=settings.model_name_openai)
  llm_groq = ChatGroq(model=settings.model_name_groq)
  return llm_openai, llm_groq