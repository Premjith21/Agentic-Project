from .base_agent import BaseAgent

class PoemAgent(BaseAgent):
    def get_agent_name(self):
        return "Poem Agent"
    
    def should_handle(self, message: str) -> bool:
        poem_keywords = [
            'poem', 'poetry', 'verse', 'rhyme', 'write a poem', 'haiku', 
            'sonnet', 'limerick', 'stanza', 'couplet', 'ode', 'ballad',
            'create a poem', 'compose a poem', 'write poetry', '4-line rhyme',
            'short poem', 'rhyming poem', 'poetic', 'verses'
        ]
        return any(keyword in message.lower() for keyword in poem_keywords)
    
    def handle_message(self, message: str, context: dict = None) -> str:
        system_msg = "You are a creative poet. Write beautiful, engaging poems using creative language and consistent structure. Focus on the requested theme and format."
        prompt = f"Write a poem about: {message}"
        return self.call_llm(prompt, system_msg)