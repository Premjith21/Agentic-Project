import streamlit as st
import requests
import time

# Configuration
BACKEND_URL = "http://localhost:5000/api"

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'user_id': None,
        'user_name': None,
        'session_id': None,
        'chat_history': [],
        'document_processed': False,
        'processing': False,
        'pending_messages': [],  # Queue for messages to process
        'processed_messages': set()  # Track processed messages
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def make_api_call(url, method='POST', json_data=None, files=None):
    """Helper function to make API calls with error handling"""
    try:
        print(f"🔄 Making API call to: {url}")
        if method == 'POST':
            if files:
                response = requests.post(url, files=files, data=json_data, timeout=30)
            else:
                response = requests.post(url, json=json_data, timeout=30)
        else:
            response = requests.get(url, timeout=30)

        print(f"📨 Response status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API call successful")
            return result, True
        else:
            print(f"❌ API error {response.status_code}: {response.text}")
            return None, False
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        return None, False

def main():
    st.set_page_config(
        page_title="AI Agent Platform",
        page_icon="🤖",
        layout="wide"
    )

    initialize_session_state()

    # Sidebar
    with st.sidebar:
        st.title("🤖 AI Agent Platform")

        if st.session_state.user_id:
            st.success(f"👋 Welcome, {st.session_state.user_name}!")
            st.info(f"User ID: {st.session_state.user_id}")

            if st.button("🚪 Logout"):
                if st.session_state.session_id:
                    make_api_call(f"{BACKEND_URL}/logout", json_data={"session_id": st.session_state.session_id})
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                initialize_session_state()
                st.rerun()

            st.markdown("---")
            st.subheader("🎯 Available Agents")
            agents = [
                "🔢 Math Agent - Solves mathematical problems",
                "📝 Poem Agent - Generates creative poems",
                "🌤️ Weather Agent - Provides weather updates",
                "💻 Code Agent - Helps with programming",
                "💰 Finance Agent - Stock prices & analysis",
                "📰 News Agent - Latest news headlines",
                "❤️ Health Agent - Wellness & fitness tips"
            ]
            for agent in agents:
                st.write(agent)

            st.markdown("---")
            page = st.radio("📍 Navigation", ["💬 Chat", "📄 Document Q&A"])
        else:
            page = "🔐 Login"

    # Page routing
    if page == "🔐 Login":
        render_login_page()
    elif page == "💬 Chat":
        render_chat_interface()
    elif page == "📄 Document Q&A":
        render_document_upload()

def render_login_page():
    st.title("🤖 AI Agent Platform")
    st.subheader("Multi-Agent AI Assistant System")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        with st.form("login_form"):
            st.subheader("Login to Your Account")
            email = st.text_input("📧 Email or Phone Number")
            password = st.text_input("🔒 Password", type="password")
            login_btn = st.form_submit_button("🚀 Login")

            if login_btn:
                if email and password:
                    with st.spinner("Logging in..."):
                        result, success = make_api_call(
                            f"{BACKEND_URL}/login",
                            json_data={"email": email, "phone": email, "password": password}
                        )
                        if success and result.get('success'):
                            st.session_state.user_id = result['user_id']
                            st.session_state.user_name = result['name']
                            st.session_state.session_id = result['session_id']
                            st.success(f"✅ Welcome back, {result['name']}!")
                            time.sleep(1)
                            st.rerun()
                        elif success:
                            st.error(f"❌ {result.get('message', 'Login failed')}")
                else:
                    st.error("❌ Please fill all fields")

    with tab2:
        with st.form("register_form"):
            st.subheader("Create New Account")
            name = st.text_input("👤 Full Name")
            email = st.text_input("📧 Email")
            phone = st.text_input("📱 Phone (optional)")
            password = st.text_input("🔒 Password", type="password")
            confirm_password = st.text_input("✅ Confirm Password", type="password")
            register_btn = st.form_submit_button("📝 Register")

            if register_btn:
                if name and (email or phone) and password:
                    if password == confirm_password:
                        with st.spinner("Creating account..."):
                            user_data = {
                                "name": name,
                                "email": email,
                                "phone": phone,
                                "password": password
                            }
                            result, success = make_api_call(
                                f"{BACKEND_URL}/register",
                                json_data=user_data
                            )
                            if success and result.get('success'):
                                st.success("✅ Registration successful! Please login.")
                            elif success:
                                st.error(f"❌ {result.get('message', 'Registration failed')}")
                    else:
                        st.error("❌ Passwords don't match")
                else:
                    st.error("❌ Please fill required fields")

def render_chat_interface():
    st.title("💬 AI Agent Chat")
    st.markdown("Chat with our specialized AI agents. They'll automatically handle your queries!")

    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant"):
            st.write(chat["agent"])
            if chat.get("agent_used"):
                st.caption(f"🤖 Agent: {chat['agent_used']}")

    if not st.session_state.chat_history:
        st.info("💡 Start a conversation! Try asking about math, poems, weather, code, finance, news, or health topics.")

    # Chat input
    user_input = st.chat_input("Type your message here...")

    # Step 1: Add new message to queue
    if user_input and user_input not in st.session_state.pending_messages and user_input not in st.session_state.processed_messages:
        st.session_state.pending_messages.append(user_input)
        st.rerun()

    # Step 2: Process messages from queue
    if st.session_state.pending_messages and not st.session_state.processing:
        current_message = st.session_state.pending_messages[0]
        
        # Mark as processing
        st.session_state.processing = True
        
        # Add to chat history with thinking placeholder
        st.session_state.chat_history.append({
            "user": current_message,
            "agent": "Thinking... 🤖",
            "agent_used": "Processing"
        })
        
        # Make API call
        result, success = make_api_call(
            f"{BACKEND_URL}/chat",
            json_data={
                "session_id": st.session_state.session_id,
                "message": current_message
            }
        )
        
        # Update chat history with actual response
        if success:
            st.session_state.chat_history[-1] = {
                "user": current_message,
                "agent": result.get("response", "No response received"),
                "agent_used": result.get("agent_used", "Unknown")
            }
        else:
            st.session_state.chat_history[-1] = {
                "user": current_message,
                "agent": "❌ Failed to get response from AI agent. Please try again.",
                "agent_used": "Error"
            }
        
        # Move message from pending to processed
        st.session_state.pending_messages.pop(0)
        st.session_state.processed_messages.add(current_message)
        st.session_state.processing = False
        
        st.rerun()

def render_document_upload():
    st.title("📄 Document Q&A")
    st.markdown("Upload documents and ask questions about their content!")

    if not st.session_state.session_id:
        st.error("❌ Please login first to use Document Q&A")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📤 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF or Word document",
            type=['pdf', 'docx'],
            help="Supported formats: PDF, Word documents"
        )

        if uploaded_file:
            st.info(f"📄 Selected file: {uploaded_file.name}")

            if st.button("🚀 Process Document"):
                with st.spinner("Processing document..."):
                    files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    data = {'session_id': st.session_state.session_id}

                    result, success = make_api_call(
                        f"{BACKEND_URL}/upload-document",
                        files=files,
                        json_data=data
                    )

                    if success and result.get('success'):
                        st.session_state.document_processed = True
                        st.success("✅ Document processed successfully!")
                    else:
                        st.error("❌ Failed to process document")

    with col2:
        st.subheader("❓ Ask Questions")

        if not st.session_state.document_processed:
            st.warning("📝 Please upload and process a document first.")
        else:
            question = st.text_area(
                "Your question about the document",
                placeholder="What would you like to know about the document?",
                height=100
            )

            if st.button("🔍 Get Answer"):
                if question:
                    with st.spinner("Searching for answer..."):
                        result, success = make_api_call(
                            f"{BACKEND_URL}/query-document",
                            json_data={
                                "session_id": st.session_state.session_id,
                                "question": question
                            }
                        )
                        if success:
                            st.success("✅ Answer found!")
                            st.write(result.get("answer", "No answer found"))
                        else:
                            st.error("❌ Failed to get answer")
                else:
                    st.error("❌ Please enter a question")

if __name__ == "__main__":
    main()