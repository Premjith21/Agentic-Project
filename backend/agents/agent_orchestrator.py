from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator
from .math_agent import MathAgent
from .poem_agent import PoemAgent
from .weather_agent import WeatherAgent
from .code_agent import CodeAgent
from .finance_agent import FinanceAgent
from .news_agent import NewsAgent
from .health_agent import HealthAgent

# Define the state for our agent system
class AgentState(TypedDict):
    user_id: str
    session_id: str
    message: str
    selected_agent: str
    response: str
    agent_used: str
    history: Annotated[list, operator.add]
    error: str
    context: dict

class AgentOrchestrator:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        
        # Initialize all agents
        self.agents = {
            "math_agent": MathAgent(),
            "code_agent": CodeAgent(),
            "finance_agent": FinanceAgent(),
            "health_agent": HealthAgent(),
            "poem_agent": PoemAgent(),
            "weather_agent": WeatherAgent(),
            "news_agent": NewsAgent()
        }
        
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()
        print("✅ LangGraph AgentOrchestrator initialized with graph workflow")

    def _build_workflow(self):
        """Build the LangGraph workflow with conditional routing"""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("router", self._route_message)
        workflow.add_node("math_agent", self._call_math_agent)
        workflow.add_node("code_agent", self._call_code_agent)
        workflow.add_node("finance_agent", self._call_finance_agent)
        workflow.add_node("health_agent", self._call_health_agent)
        workflow.add_node("poem_agent", self._call_poem_agent)
        workflow.add_node("weather_agent", self._call_weather_agent)
        workflow.add_node("news_agent", self._call_news_agent)
        workflow.add_node("fallback_agent", self._call_fallback_agent)
        workflow.add_node("store_memory", self._store_in_memory)
        
        # Set the entry point
        workflow.set_entry_point("router")
        
        # Add conditional edges from router
        workflow.add_conditional_edges(
            "router",
            self._should_route_to_agent,
            {
                "math_agent": "math_agent",
                "code_agent": "code_agent",
                "finance_agent": "finance_agent",
                "health_agent": "health_agent",
                "poem_agent": "poem_agent",
                "weather_agent": "weather_agent",
                "news_agent": "news_agent",
                "fallback_agent": "fallback_agent"
            }
        )
        
        # Connect all agent nodes to memory storage
        for agent_name in self.agents.keys():
            workflow.add_edge(agent_name, "store_memory")
        workflow.add_edge("fallback_agent", "store_memory")
        
        # Connect memory storage to end
        workflow.add_edge("store_memory", END)
        
        return workflow.compile()

    def _route_message(self, state: AgentState) -> AgentState:
        """Router node - prepares context and determines initial routing"""
        print(f"🔍 Routing message: '{state['message']}'")
        
        # Get conversation history
        history = self.memory_manager.get_conversation_history(
            state['user_id'], state['session_id']
        )
        
        return {
            **state,
            "history": history,
            "context": {
                "user_id": state['user_id'],
                "session_id": state['session_id'],
                "history": history
            }
        }

    def _should_route_to_agent(self, state: AgentState) -> str:
        """Conditional routing logic - determines which agent to use"""
        message_lower = state['message'].lower()
        
        # Priority-based routing (same logic as before)
        if MathAgent().should_handle(message_lower):
            return "math_agent"
        elif CodeAgent().should_handle(message_lower):
            return "code_agent"
        elif FinanceAgent().should_handle(message_lower):
            return "finance_agent"
        elif HealthAgent().should_handle(message_lower):
            return "health_agent"
        elif PoemAgent().should_handle(message_lower):
            return "poem_agent"
        elif WeatherAgent().should_handle(message_lower):
            return "weather_agent"
        elif NewsAgent().should_handle(message_lower):
            return "news_agent"
        else:
            return "fallback_agent"

    # Agent node functions
    def _call_math_agent(self, state: AgentState) -> AgentState:
        print("🎯 Executing Math Agent")
        agent = self.agents["math_agent"]
        response = agent.handle_message(state['message'], state['context'])
        return {**state, "response": response, "agent_used": "Math Agent", "selected_agent": "math_agent"}

    def _call_code_agent(self, state: AgentState) -> AgentState:
        print("🎯 Executing Code Agent")
        agent = self.agents["code_agent"]
        response = agent.handle_message(state['message'], state['context'])
        return {**state, "response": response, "agent_used": "Code Agent", "selected_agent": "code_agent"}

    def _call_finance_agent(self, state: AgentState) -> AgentState:
        print("🎯 Executing Finance Agent")
        agent = self.agents["finance_agent"]
        response = agent.handle_message(state['message'], state['context'])
        return {**state, "response": response, "agent_used": "Finance Agent", "selected_agent": "finance_agent"}

    def _call_health_agent(self, state: AgentState) -> AgentState:
        print("🎯 Executing Health Agent")
        agent = self.agents["health_agent"]
        response = agent.handle_message(state['message'], state['context'])
        return {**state, "response": response, "agent_used": "Health Agent", "selected_agent": "health_agent"}

    def _call_poem_agent(self, state: AgentState) -> AgentState:
        print("🎯 Executing Poem Agent")
        agent = self.agents["poem_agent"]
        response = agent.handle_message(state['message'], state['context'])
        return {**state, "response": response, "agent_used": "Poem Agent", "selected_agent": "poem_agent"}

    def _call_weather_agent(self, state: AgentState) -> AgentState:
        print("🎯 Executing Weather Agent")
        agent = self.agents["weather_agent"]
        response = agent.handle_message(state['message'], state['context'])
        return {**state, "response": response, "agent_used": "Weather Agent", "selected_agent": "weather_agent"}

    def _call_news_agent(self, state: AgentState) -> AgentState:
        print("🎯 Executing News Agent")
        agent = self.agents["news_agent"]
        response = agent.handle_message(state['message'], state['context'])
        return {**state, "response": response, "agent_used": "News Agent", "selected_agent": "news_agent"}

    def _call_fallback_agent(self, state: AgentState) -> AgentState:
        print("🤖 Using Fallback Agent")
        response = (
            "I'm sorry, this question is outside my domain expertise. "
            "I can help with:\n"
            "• 🔢 Math problems and calculations\n"
            "• 📝 Creative writing and poems\n" 
            "• 🌤️ Weather information and forecasts\n"
            "• 💻 Programming and code help\n"
            "• 💰 Finance and stock information\n"
            "• 📰 Latest news headlines\n"
            "• ❤️ Health and wellness tips\n"
            "• 📄 Questions about uploaded documents"
        )
        return {**state, "response": response, "agent_used": "Fallback", "selected_agent": "fallback_agent"}

    def _store_in_memory(self, state: AgentState) -> AgentState:
        """Store the interaction in memory"""
        print("💾 Storing interaction in memory")
        self.memory_manager.store_interaction(
            state['user_id'],
            state['session_id'],
            state['message'],
            state['response'],
            state['agent_used']
        )
        return state

    def process_message(self, user_id: str, message: str, session_id: str = "default") -> Dict[str, Any]:
        """Process a message using the LangGraph workflow"""
        try:
            print(f"🔄 LangGraph processing message for user {user_id}: '{message}'")
            
            # Prepare initial state
            initial_state: AgentState = {
                "user_id": user_id,
                "session_id": session_id,
                "message": message,
                "selected_agent": "",
                "response": "",
                "agent_used": "",
                "history": [],
                "error": "",
                "context": {}
            }
            
            # Execute the LangGraph workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Prepare result
            result = {
                "response": final_state["response"],
                "agent_used": final_state["agent_used"],
                "session_id": session_id
            }
            
            print(f"🎉 LangGraph result: {result}")
            return result
            
        except Exception as e:
            print(f"💥 Error in LangGraph process_message: {e}")
            import traceback
            traceback.print_exc()
            
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            return {
                "response": error_response,
                "agent_used": "Error",
                "session_id": session_id
            }