"""
Test script for config endpoints
Run this script after the server is started: python -m uvicorn app.main:app --reload --port 8000
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# You need to replace this with a valid tenant JWT token
# You can get one by:
# 1. Signing up: POST /api/v1/auth/signup with {"email": "test@example.com", "password": "password123"}
# 2. Logging in: POST /api/v1/auth/login with {"email": "test@example.com", "password": "password123"}
# 3. Use the access_token from the response

# For testing, replace with your actual token
# TENANT_TOKEN = "your_jwt_token_here"
TENANT_TOKEN = None

def test_save_config():
    """Test saving chatbot config for a tenant"""
    print("\n=== Test 1: Save Config (PUT /config) ===")
    
    if not TENANT_TOKEN:
        print("❌ TENANT_TOKEN not set. Please set a valid JWT token first.")
        return False
    
    headers = {
        "Authorization": f"Bearer {TENANT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    config_data = {
        "name": "Support Bot",
        "greeting_msg": "Hello! How can I help you today?",
        "rounded": True,
        "theme": {
            "primaryColor": "#007bff",
            "secondaryColor": "#6c757d",
            "backgroundColor": "#ffffff"
        }
    }
    
    try:
        response = requests.put(f"{BASE_URL}/config/", json=config_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Config saved successfully!")
            return True
        else:
            print(f"❌ Failed to save config")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_config():
    """Test retrieving chatbot config for a tenant"""
    print("\n=== Test 2: Get Config (GET /config) ===")
    
    if not TENANT_TOKEN:
        print("❌ TENANT_TOKEN not set. Please set a valid JWT token first.")
        return False
    
    headers = {
        "Authorization": f"Bearer {TENANT_TOKEN}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/config/", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Config retrieved successfully!")
            return True
        elif response.status_code == 404:
            print("ℹ️ No config found (expected if not created yet)")
            return True
        else:
            print(f"❌ Failed to get config")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_update_config():
    """Test updating existing chatbot config"""
    print("\n=== Test 3: Update Config (PUT /config) ===")
    
    if not TENANT_TOKEN:
        print("❌ TENANT_TOKEN not set. Please set a valid JWT token first.")
        return False
    
    headers = {
        "Authorization": f"Bearer {TENANT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    updated_config = {
        "name": "Support Bot v2",
        "greeting_msg": "Welcome! How may I assist you?",
        "rounded": False,
        "theme": {
            "primaryColor": "#28a745",
            "secondaryColor": "#ffc107"
        }
    }
    
    try:
        response = requests.put(f"{BASE_URL}/config/", json=updated_config, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Config updated successfully!")
            return True
        else:
            print(f"❌ Failed to update config")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check():
    """Test if server is running"""
    print("\n=== Health Check ===")
    try:
        response = requests.get(f"http://localhost:8000/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            print("✅ Server is running!")
            return True
        else:
            print("❌ Server health check failed")
            return False
    except Exception as e:
        print(f"❌ Server is not running or unreachable: {e}")
        return False

def main():
    print("=" * 60)
    print("Config Endpoints Test Script")
    print("=" * 60)
    
    # Check if server is running
    if not test_health_check():
        print("\n⚠️ Server is not running. Please start it with:")
        print("python -m uvicorn app.main:app --reload --port 8000")
        return
    
    if not TENANT_TOKEN:
        print("\n⚠️ TENANT_TOKEN is not set!")
        print("\nTo test the endpoints, you need a valid JWT token:")
        print("1. Sign up a user via POST /api/v1/auth/signup")
        print("2. Log in via POST /api/v1/auth/login")
        print("3. Copy the access_token and set TENANT_TOKEN variable in this script")
        print("\nManual test commands:")
        print(f"\n# Save config:")
        print(f'curl -X PUT {BASE_URL}/config/ \\')
        print(f'  -H "Authorization: Bearer YOUR_TOKEN" \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f'  -d \'{{"name": "Bot", "greeting_msg": "Hi!", "rounded": true, "theme": {{"color": "#000"}}}}\'')
        print(f"\n# Get config:")
        print(f'curl -X GET {BASE_URL}/config/ \\')
        print(f'  -H "Authorization: Bearer YOUR_TOKEN"')
        return
    
    # Run tests
    results = []
    results.append(test_save_config())
    results.append(test_get_config())
    results.append(test_update_config())
    results.append(test_get_config())  # Get again to verify update
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print(f"❌ {total - passed} test(s) failed")

if __name__ == "__main__":
    main()
