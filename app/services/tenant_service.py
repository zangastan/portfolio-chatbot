from typing import List
from app.repositories.tenant_repo import TenantRepository
from app.core.database import supabase
from app.models.tenant import Tenant

class TenantService:
    def __init__(self):
        self.repo = TenantRepository(supabase)
        from app.repositories.user_repo import UserRepository
        self.user_repo = UserRepository(supabase)
    
    def createApi (self , tenant_id: str):
        if not tenant_id:
            raise Exception("Tenant ID is required")
        

    def create_tenant(self, name: str, admin_user_id: str = None, admin_email: str = None) -> Tenant:
        tenant = self.repo.create({"name": name})
        
        if admin_user_id and admin_email:
            # 1. Update or Create the admin user record in our DB
            existing_user = self.user_repo.get_by_id(admin_user_id)
            user_data = {
                "id": admin_user_id,
                "email": admin_email,
                "role": "admin",
                "tenant_id": str(tenant.id)
            }
            
            if existing_user:
                print(f"DEBUG: User {admin_user_id} exists. Updating tenant_id to {tenant.id}")
                self.user_repo.update(admin_user_id, user_data)
            else:
                print(f"DEBUG: Creating new user record for {admin_user_id}")
                self.user_repo.create(user_data)
            
            # 2. Update Supabase Auth metadata for the user (so future tokens have tenant_id)
            # using supabase.auth.update_user because we are acting as the user (admin_user_id)
            try:
                supabase.auth.update_user({
                    "data": {"tenant_id": str(tenant.id)}
                })
            except Exception as e:
                print(f"Warning: Failed to update auth metadata: {e}")
            
        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        return self.repo.get_by_id(tenant_id)
