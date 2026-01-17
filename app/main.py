from fastapi import FastAPI
from app.core.config import settings
from app.routes import auth, tenants, conversations, messages, automation, tickets, knowledge, analytics, api_keys, config
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your Next.js app URL
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
# app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Auth"])
# app.include_router(api_keys.router, prefix=settings.API_V1_STR + "/api-keys", tags=["API Keys"])
# app.include_router(tenants.router, prefix=settings.API_V1_STR)
# app.include_router(conversations.router, prefix=settings.API_V1_STR)
app.include_router(messages.router, prefix=settings.API_V1_STR)
app.include_router(automation.router, prefix=settings.API_V1_STR)
# app.include_router(tickets.router, prefix=settings.API_V1_STR)
app.include_router(knowledge.router, prefix=settings.API_V1_STR)
# app.include_router(analytics.router, prefix=settings.API_V1_STR)
# app.include_router(config.router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to IcoBot Backend API"}
