from typing import List, Tuple, Optional
from app.services.automation_service import AutomationService

class MessageService:
    def __init__(self):
        self.automation_service = AutomationService()

    async def send_message(self, content: str) -> Tuple[str, dict]:
        """
        Processes a user message and returns the AI response.
        """
        print(f"DEBUG: Processing message: {content}")
        
        ai_result = await self.automation_service.generate_response(content)
        print(f"DEBUG: AI Result: {ai_result}")
        
        return content, ai_result

    def list_messages(self, conversation_id: str) -> List:
        # Persistence removed in this simplified version
        return []
