from .base_agent import BaseAgent

class HealthAgent(BaseAgent):
    def get_agent_name(self):
        return "Health Agent"
    
    def should_handle(self, message: str) -> bool:
        health_keywords = [
            'health', 'fitness', 'diet', 'exercise', 'nutrition', 'wellness',
            'sleep', 'quality', 'insomnia', 'rest', 'bedtime', 'dream',
            'workout', 'gym', 'yoga', 'meditation', 'mental', 'therapy',
            'doctor', 'hospital', 'medicine', 'vitamin', 'supplement',
            'protein', 'carbohydrate', 'calorie', 'weight', 'obesity',
            'muscle', 'strength', 'cardio', 'aerobic', 'anaerobic',
            'recovery', 'injury', 'pain', 'headache', 'fever', 'cold',
            'flu', 'allergy', 'asthma', 'diabetes', 'heart', 'blood',
            'pressure', 'cholesterol', 'cancer', 'covid', 'pandemic',
            'immune', 'immunity', 'boost immune', 'back pain', 'exercise',
            'fitness', 'workout routine', 'healthy', 'wellbeing', 'lifestyle',
            'diet plan', 'nutrition tips', 'weight loss', 'weight gain',
            'muscle building', 'fat loss', 'cardio workout', 'strength training',
            'flexibility', 'mobility', 'stress relief', 'anxiety', 'depression',
            'mental health', 'self care', 'healthy habits', 'prevention'
        ]
        return any(keyword in message.lower() for keyword in health_keywords)
    
    def handle_message(self, message: str, context: dict = None) -> str:
        system_msg = """You are a health and wellness advisor. Provide general health information, fitness tips, and wellness advice. 
        Always include a disclaimer that you are not a medical professional and recommend consulting healthcare providers for medical advice.
        Be specific, practical, and provide actionable tips."""
        
        disclaimer = "\n\n⚠️ Disclaimer: I am an AI assistant and not a medical professional. Please consult healthcare providers for medical advice."
        
        prompt = f"Provide health and wellness information about: {message}"
        response = self.call_llm(prompt, system_msg)
        return response + disclaimer