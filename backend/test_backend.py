import requests
import json

def test_backend():
    print("🧪 Testing Backend API...")
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:5000/api/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test if we can register a user
    try:
        test_user = {
            "name": "Test User",
            "email": "test@test.com", 
            "password": "test123"
        }
        response = requests.post("http://localhost:5000/api/register", json=test_user)
        print(f"✅ Registration test: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Registration test failed: {e}")
    
    return True

if __name__ == "__main__":
    test_backend()