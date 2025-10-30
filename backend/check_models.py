from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    try:
        models = client.models.list()
        print("✅ Available Groq Models:")
        for model in models.data:
            print(f"  - {model.id}")
        return [model.id for model in models.data]
    except Exception as e:
        print(f"❌ Error fetching models: {e}")
        return []

if __name__ == "__main__":
    list_available_models()