from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.agent_orchestrator import AgentOrchestrator  # ✅ Only one import
from auth.auth import authenticate_user, register_user
from auth.session_manager import SessionManager
from memory.memory_manager import MemoryManager
from document_qa.document_processor import DocumentProcessor
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

# Initialize components
try:
    memory_manager = MemoryManager()
    agent_orchestrator = AgentOrchestrator(memory_manager)
    document_processor = DocumentProcessor()
    session_manager = SessionManager()
    logger.info("All components initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize components: {e}")
    raise

@app.route('/')
def home():
    return jsonify({"message": "AI Agent Platform API is running!", "status": "healthy"})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No JSON data provided"}), 400
        
        result = register_user(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No JSON data provided"}), 400
        
        result = authenticate_user(data)
        
        if result['success']:
            session_id = session_manager.create_session(
                result['user_id'], 
                {'name': result['name']}
            )
            result['session_id'] = session_id
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            print("❌ No JSON data received")
            return jsonify({'error': 'No JSON data provided'}), 400
        
        session_id = data.get('session_id')
        message = data.get('message')
        
        print(f"📨 Received request - Session: {session_id}, Message: '{message}'")
        
        if not session_id or not message:
            print("❌ Missing session_id or message")
            return jsonify({'error': 'Missing session_id or message'}), 400
        
        session = session_manager.get_session(session_id)
        if not session:
            print("❌ Invalid or expired session")
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        user_id = session['user_id']
        print(f"✅ Valid session for user: {user_id}")
        
        print(f"🔍 Processing message through agent orchestrator...")
        response = agent_orchestrator.process_message(user_id, message, session_id)
        
        print(f"📤 Sending response: {response}")
        return jsonify(response)
        
    except Exception as e:
        print(f"💥 Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'response': f"I apologize, but I encountered an error: {str(e)}",
            'agent_used': 'Error', 
            'session_id': data.get('session_id') if data else 'unknown'
        }), 500
@app.route('/api/upload-document', methods=['POST'])
def upload_document():
    try:
        session_id = request.form.get('session_id')
        file = request.files.get('file')
        
        if not file or not session_id:
            return jsonify({'error': 'Missing file or session_id'}), 400
        
        session = session_manager.get_session(session_id)
        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        user_id = session['user_id']
        result = document_processor.process_document(user_id, file)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Document upload error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/query-document', methods=['POST'])
def query_document():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        session_id = data.get('session_id')
        question = data.get('question')
        
        if not session_id or not question:
            return jsonify({'error': 'Missing session_id or question'}), 400
        
        session = session_manager.get_session(session_id)
        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        user_id = session['user_id']
        result = document_processor.query_document(user_id, question)
        return jsonify({"answer": result})
    except Exception as e:
        logger.error(f"Document query error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    try:
        data = request.get_json()
        session_id = data.get('session_id') if data else None
        
        if session_id:
            session_manager.delete_session(session_id)
        
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'service': 'AI Agent Platform',
        'agents': ['Math', 'Poem', 'Weather', 'Code', 'Finance', 'News', 'Health']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)