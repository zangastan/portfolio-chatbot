from app.schemas.user import LoginRequest, Token

def login(request: LoginRequest) -> Token:
    return Token(access_token="stub_token", token_type="bearer")

def logout():
    return {"message": "Logged out successfully"}
