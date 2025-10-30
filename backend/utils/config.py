import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')