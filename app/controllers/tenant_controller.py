from app.schemas.tenant import TenantResponse, TenantSettingsUpdate

def get_tenant_me() -> TenantResponse:
    return TenantResponse(
        id="stub_tenant_id", 
        name="Stub Tenant", 
        created_at="2023-01-01T00:00:00"
    )

def update_tenant_settings(settings: TenantSettingsUpdate):
    return {"message": "Settings updated", "settings": settings.dict(exclude_unset=True)}
