from .base_agent import BaseAgent
import re

class MathAgent(BaseAgent):
    def get_agent_name(self):
        return "Math Agent"
    
    def should_handle(self, message: str) -> bool:
        message_lower = message.lower().strip()
        
        # Common math patterns
        math_patterns = [
            # Basic arithmetic: "123 + 456", "5*3", "10/2"
            r'\d+\s*[\+\-\*\/\=]\s*\d+',
            # Questions with numbers: "what is 123 + 456", "calculate 5 times 3"
            r'(what|calculate|solve|find).*\d+',
            # Direct math questions: "add 5 and 3", "subtract 10 from 20"
            r'(add|plus|sum|total|subtract|minus|multiply|times|divide).*\d+',
            # Percentage questions: "what is 20% of 100"
            r'\d+\s*%.*(of|from)',
            # Simple number questions that are likely math
            r'^\d+[\+\-\*\/]\d+$'
        ]
        
        # Check if any pattern matches
        for pattern in math_patterns:
            if re.search(pattern, message_lower):
                return True
        
        # Check for math keywords in context
        math_keywords = [
            'calculate', 'solve', 'math', 'equation', 'formula', 'algebra',
            'calculus', 'statistics', 'probability', 'trigonometry', 'geometry',
            'addition', 'subtraction', 'multiplication', 'division', 'add', 'plus',
            'minus', 'times', 'multiply', 'divide', 'sum', 'total', 'equals',
            'answer', 'result', 'solution'
        ]
        
        # If message contains numbers and math keywords, it's likely math
        has_numbers = bool(re.search(r'\d+', message_lower))
        has_math_keywords = any(keyword in message_lower for keyword in math_keywords)
        
        # ADD THIS: Handle simple word problems with numbers
        word_problem_indicators = [
            'has', 'gives', 'left', 'more', 'less', 'total', 'together', 
            'each', 'share', 'divided', 'combined', 'remaining', 'spent',
            'bought', 'sold', 'cost', 'price', 'amount'
        ]
        if has_numbers and any(indicator in message_lower for indicator in word_problem_indicators):
            return True
        
        return has_numbers and has_math_keywords
    
    def handle_message(self, message: str, context: dict = None) -> str:
        system_msg = """You are a helpful math expert. Provide clear, step-by-step solutions to mathematical problems. 
        For simple calculations, give the direct answer first, then show the steps if helpful.
        Be accurate and educational in your explanations."""
        
        prompt = f"Please solve this mathematical problem: {message}"
        return self.call_llm(prompt, system_msg)