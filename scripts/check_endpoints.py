import requests
import uuid
import sys
import time
import random
import string

BASE_URL = "http://127.0.0.1:8000/api/v1"

def random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def run_test():
    print("Starting Comprehensive Endpoint Check...")
    
    # 1. Auth - Signup
    email = f"test_user_{random_string()}@example.com"
    password = "testpassword123"
    print(f"\n[1] Testing Signup with {email}...")
    try:
        r = requests.post(f"{BASE_URL}/auth/signup", json={"email": email, "password": password})
        if r.status_code not in [200, 201]:
            print(f"FAILED: Status {r.status_code}, Response: {r.text}")
            return
        print("SUCCESS: Signup successful.")
        user_data = r.json()
    except Exception as e:
        print(f"FAILED: Exception {e}")
        return

    # 2. Auth - Login
    print("\n[2] Testing Login...")
    try:
        # Try both endpoints just in case
        r = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
        if r.status_code != 200:
             # Fallback to json login if token endpoint fails (though we fixed it)
             r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        
        if r.status_code != 200:
            print(f"FAILED: Status {r.status_code}, Response: {r.text}")
            return
            
        data = r.json()
        token = data.get("access_token")
        if not token:
            print("FAILED: No access token returned.")
            return
        print("SUCCESS: Login successful. Token retrieved.")
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"FAILED: Exception {e}")
        return

    # 3. Create Tenant
    print("\n[3] Testing Create Tenant...")
    tenant_id = None
    try:
        tenant_name = f"Test Tenant {random_string()}"
        r = requests.post(f"{BASE_URL}/tenants/", json={"name": tenant_name}, headers=headers)
        if r.status_code != 200:
            print(f"FAILED: Status {r.status_code}, Response: {r.text}")
        else:
            tenant_data = r.json()
            tenant_id = tenant_data.get("id")
            print(f"SUCCESS: Tenant created. ID: {tenant_id}")
            
            # RE-LOGIN to refresh token with new metadata (tenant_id)
            print("  -> Refreshing token to get tenant_id in metadata...")
            r_login = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
            if r_login.status_code == 200:
                token = r_login.json().get("access_token")
                headers = {"Authorization": f"Bearer {token}"}
                print("  -> Token refreshed.")
            else:
                 print("  -> Failed to refresh token.")
    except Exception as e:
        print(f"FAILED: Exception {e}")

    # 4. Create Conversation
    print("\n[4] Testing Create Conversation...")
    conversation_id = None
    try:
        r = requests.post(f"{BASE_URL}/conversations/", json={"visitor_id": "vis-001"}, headers=headers)
        if r.status_code != 200:
            print(f"FAILED: Status {r.status_code}, Response: {r.text}")
        else:
            conv_data = r.json()
            conversation_id = conv_data.get("id")
            print(f"SUCCESS: Conversation created. ID: {conversation_id}")
    except Exception as e:
        print(f"FAILED: Exception {e}")

    # 5. Send Message (Trigger AI)
    if conversation_id:
        print("\n[5] Testing Send Message...")
        try:
            r = requests.post(f"{BASE_URL}/messages/", json={
                "conversation_id": conversation_id,
                "content": "Hello, this is a test message.",
                "sender_type": "visitor"
            }, headers=headers)
            if r.status_code != 200:
                print(f"FAILED: Status {r.status_code}, Response: {r.text}")
            else:
                msg_data = r.json()
                print("SUCCESS: Message sent.")
        except Exception as e:
            print(f"FAILED: Exception {e}")

    # 6. Create Ticket
    if conversation_id:
        print("\n[6] Testing Create Ticket...")
        ticket_id = None
        try:
            r = requests.post(f"{BASE_URL}/tickets/", json={
                "conversation_id": conversation_id,
                "priority": "high",
                "description": "Test ticket"
            }, headers=headers)
            if r.status_code != 200:
                print(f"FAILED: Status {r.status_code}, Response: {r.text}")
            else:
                tick_data = r.json()
                ticket_id = tick_data.get("id")
                print(f"SUCCESS: Ticket created. ID: {ticket_id}")
        except Exception as e:
            print(f"FAILED: Exception {e}")

    # 7. Add Knowledge Base Doc
    print("\n[7] Testing Add Knowledge Document...")
    try:
        r = requests.post(f"{BASE_URL}/knowledge/", json={
            "title": "Welcome Guide",
            "content": "This is a test document for the knowledge base."
        }, headers=headers)
        if r.status_code != 200:
            print(f"FAILED: Status {r.status_code}, Response: {r.text}")
        else:
            print("SUCCESS: Document added.")
    except Exception as e:
        print(f"FAILED: Exception {e}")

if __name__ == "__main__":
    run_test()
