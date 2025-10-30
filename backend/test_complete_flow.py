import requests
import json

def test_complete_chat_flow():
    print("🧪 Testing Complete Chat Flow...")
    
    # Test data
    test_user = {
        "name": "Flow Test User",
        "email": "flowtest@test.com", 
        "password": "test123"
    }
    
    # Step 1: Register
    print("1. Registering user...")
    response = requests.post("http://localhost:5000/api/register", json=test_user)
    print(f"   Registration: {response.status_code} - {response.json()}")
    
    # Step 2: Login
    print("2. Logging in...")
    login_data = {
        "email": "flowtest@test.com",
        "password": "test123"
    }
    response = requests.post("http://localhost:5000/api/login", json=login_data)
    login_result = response.json()
    print(f"   Login: {response.status_code} - {login_result}")
    
    if login_result.get('success'):
        session_id = login_result.get('session_id')
        
        # Step 3: Send chat message
        print("3. Sending chat message...")
        chat_data = {
            "session_id": session_id,
            "message": "what is 234 + 582"
        }
        
        print(f"   Chat request: {chat_data}")
        response = requests.post("http://localhost:5000/api/chat", json=chat_data)
        print(f"   Chat response status: {response.status_code}")
        
        if response.status_code == 200:
            chat_result = response.json()
            print(f"   ✅ Chat response: {chat_result}")
        else:
            print(f"   ❌ Chat failed: {response.text}")
            
    else:
        print("❌ Login failed")

if __name__ == "__main__":
    test_complete_chat_flow()