from fastapi import FastAPI
from app.core.config import settings
from app.routes import messages
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Augustine's Assistant API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Chatbot Router
app.include_router(messages.router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to Augustine's Personal Assistant API"}
