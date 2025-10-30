from abc import ABC, abstractmethod
from groq import Groq
import os

class BaseAgent(ABC):
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        # List of CURRENTLY AVAILABLE models (from your check_models.py)
        self.available_models = [
            "llama-3.3-70b-versatile",    # Most powerful available
            "llama-3.1-8b-instant",       # Fast and reliable
            "gemma2-9b-it",               # Google's model
            "qwen/qwen3-32b",             # Alternative model
        ]
    
    @abstractmethod
    def get_agent_name(self):
        pass
    
    @abstractmethod
    def should_handle(self, message: str) -> bool:
        pass
    
    @abstractmethod
    def handle_message(self, message: str, context: dict = None) -> str:
        pass
    
    def call_llm(self, prompt: str, system_message: str = None) -> str:
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})
        
        # Try each model until one works
        for model in self.available_models:
            try:
                print(f"🤖 [{self.get_agent_name()}] Trying model: {model}")
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                print(f"✅ [{self.get_agent_name()}] Model {model} succeeded!")
                return response.choices[0].message.content
            except Exception as e:
                print(f"❌ [{self.get_agent_name()}] Model {model} failed: {str(e)}")
                continue  # Try next model
        
        return f"Error: All available models failed for {self.get_agent_name()}. Please check your Groq API configuration."