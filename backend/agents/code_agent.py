from .base_agent import BaseAgent

class CodeAgent(BaseAgent):
    def get_agent_name(self):
        return "Code Agent"
    
    def should_handle(self, message: str) -> bool:
        code_keywords = [
            'code', 'programming', 'function', 'debug', 'python', 'javascript', 'java',
            'c++', 'html', 'css', 'sql', 'algorithm', 'bubble sort', 'quick sort',
            'merge sort', 'binary search', 'data structure', 'stack', 'queue',
            'linked list', 'array', 'variable', 'loop', 'if statement', 'class',
            'object', 'api', 'framework', 'library', 'compile', 'syntax', 'error',
            'exception', 'try catch', 'git', 'github', 'docker', 'kubernetes',
            'backend', 'frontend', 'fullstack', 'web development', 'mobile app',
            'database', 'mysql', 'mongodb', 'postgresql', 'orm', 'rest api',
            'graphql', 'authentication', 'authorization', 'encryption', 'security',
            'for loop', 'while loop', 'method', 'parameter', 'return', 'import',
            'package', 'module', 'script', 'development', 'software', 'application'
        ]
        return any(keyword in message.lower() for keyword in code_keywords)
    
    def handle_message(self, message: str, context: dict = None) -> str:
        system_msg = "You are an expert programming assistant. Help with code generation, debugging, and explanations. Provide clean, efficient code with examples."
        prompt = f"Help with this programming request: {message}"
        return self.call_llm(prompt, system_msg)