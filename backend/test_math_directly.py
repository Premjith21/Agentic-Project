from agents.math_agent import MathAgent
import os
from dotenv import load_dotenv

load_dotenv()

def test_math_agent():
    print("🧪 Testing Math Agent Directly...")
    
    try:
        math_agent = MathAgent()
        
        # Test questions
        test_questions = [
            "what is 41 + 63",
            "calculate 850 + 963", 
            "22 + 98",
            "add 5 and 3"
        ]
        
        for question in test_questions:
            print(f"\n" + "="*50)
            print(f"Testing: '{question}'")
            print("="*50)
            
            # Test detection
            should_handle = math_agent.should_handle(question)
            print(f"Should handle: {should_handle}")
            
            if should_handle:
                response = math_agent.handle_message(question)
                print(f"Response: {response}")
            else:
                print("❌ Math agent didn't handle this question")
                
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_math_agent()