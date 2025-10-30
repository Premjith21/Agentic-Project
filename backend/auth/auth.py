import hashlib
import json
import os
from datetime import datetime

USER_DB_FILE = "users.json"

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(user_data):
    users = load_users()
    
    email = user_data.get('email')
    phone = user_data.get('phone')
    name = user_data.get('name')
    password = user_data.get('password')
    
    if not (email or phone) or not name or not password:
        return {"success": False, "message": "Missing required fields"}
    
    user_id = email or phone
    if user_id in users:
        return {"success": False, "message": "User already exists"}
    
    users[user_id] = {
        "name": name,
        "password_hash": hash_password(password),
        "email": email,
        "phone": phone,
        "created_at": datetime.now().isoformat()
    }
    
    save_users(users)
    return {"success": True, "message": "User registered successfully", "user_id": user_id}

def authenticate_user(login_data):
    users = load_users()
    
    user_id = login_data.get('email') or login_data.get('phone')
    password = login_data.get('password')
    
    if not user_id or not password:
        return {"success": False, "message": "Missing credentials"}
    
    user = users.get(user_id)
    if not user or user['password_hash'] != hash_password(password):
        return {"success": False, "message": "Invalid credentials"}
    
    return {
        "success": True, 
        "message": "Login successful",
        "user_id": user_id,
        "name": user['name']
    }