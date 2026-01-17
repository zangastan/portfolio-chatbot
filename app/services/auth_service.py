from datetime import datetime
from typing import Dict, Any
from app.repositories.user_repo import UserRepository
from app.core.database import supabase

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository(supabase)

    def login(self, data: Dict[str, str]) -> Dict[str, Any]:
        """
        Proxies login to Supabase Auth.
        """
        email = data.get("email")
        password = data.get("password")
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": response.user
        }

    def signup(self, data: Any) -> Dict[str, Any]:
        """
        Proxies signup to Supabase Auth and syncs to public users table.
        Expects UserCreate model or dict.
        """
        if hasattr(data, "dict"):
            data_dict = data.dict()
        else:
            data_dict = data
            
        email = data_dict.get("email")
        password = data_dict.get("password")
        role = data_dict.get("role", "agent")
        tenant_id = data_dict.get("tenant_id")
        
        if not email or not password:
            raise ValueError("Email and password are required")

        try:
            # 1. Determine Tenant ID first
            if not tenant_id:
                print("DEBUG: No tenant_id provided, looking for existing tenant...")
                tenants_resp = supabase.table("tenants").select("id").limit(1).execute()
                if tenants_resp.data:
                    tenant_id = tenants_resp.data[0]["id"]
                    print(f"DEBUG: Using existing tenant {tenant_id}")
                else:
                    # Create a default tenant if none exists
                    print("DEBUG: Creating default tenant...")
                    tenant_resp = supabase.table("tenants").insert({"name": "Default Tenant"}).execute()
                    tenant_id = tenant_resp.data[0]["id"]
                    print(f"DEBUG: Created default tenant {tenant_id}")

            print(f"DEBUG: Attempting Supabase Auth signup for {email} with tenant_id {tenant_id}")
            
            # 2. Sign up with tenant_id in metadata
            signup_options = {
                "data": {
                    "tenant_id": str(tenant_id),
                    "role": role
                }
            }
            response = supabase.auth.sign_up({
                "email": email, 
                "password": password,
                "options": signup_options
            })
            
            if not response.user:
                print(f"DEBUG: Signup failed or needs confirmation. Response: {response}")
                return {"message": "Signup initiated, please check your email if confirmation is enabled."}

            print(f"DEBUG: Auth success. User ID: {response.user.id}. Syncing to public.users...")
            
            # 3. Create record in public.users
            user_data = {
                "id": str(response.user.id),
                "email": str(response.user.email),
                "role": role,
                "tenant_id": str(tenant_id),
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Check if user already exists (e.g. if signup was called twice)
            existing_user = self.user_repo.get_by_id(str(response.user.id))
            if existing_user:
                self.user_repo.update(str(response.user.id), user_data)
            else:
                self.user_repo.create(user_data)
                
            print(f"DEBUG: Successfully synced user {email} to public.users")
            
            return {
                "user": response.user,
                "tenant_id": tenant_id
            }
        except Exception as e:
            print(f"DEBUG: Signup Exception: {type(e).__name__}: {str(e)}")
            raise e
