from datetime import datetime
from typing import List
from app.repositories.message_repo import MessageRepository
from app.models.message import Message
from app.core.database import supabase

from app.services.automation_service import AutomationService
from app.services.knowledge_service import KnowledgeService
from app.services.ticket_service import TicketService
from app.services.analytics_service import AnalyticsService
from app.services.conversation_service import ConversationService
class MessageService:
    def __init__(self):
        self.repo = MessageRepository(supabase)
        self.automation_service = AutomationService()
        self.knowledge_service = KnowledgeService()
        self.ticket_service = TicketService()
        self.analytics_service = AnalyticsService()
        self.conversation_service = ConversationService()

    async def send_message(self, content: str):
        # 1. Save the incoming message
        # message = self.repo.create({
        #     "content": content,
        #     "created_at": datetime.utcnow().isoformat()
        # })
        
        # Track event
        # self.analytics_service.track_event(tenant_id, "message_sent", {"conversation_id": conversation_id, "sender": sender_type})

        ai_message = None
        message = content

        # 2. If visitor, trigger AI
     
        # Generate AI Response
        print("DEBUG: Requesting AI response...")
        
        ai_result = await self.automation_service.generate_response(content)
        print(f"DEBUG: AI Result: {ai_result}")
        
        response_text = ai_result.get("response", "I could not generate a response.")
        confidence = ai_result.get("confidence", 0.0)

        # # 3. Save AI Message
        # print(f"DEBUG: Saving AI message: {response_text}")
        # ai_message = self.repo.create({
        #     "tenant_id": tenant_id,
        #     "conversation_id": conversation_id,
        #     "sender_type": "bot",
        #     "content": response_text,
        #     "created_at": datetime.utcnow().isoformat(),
        #     "metadata": {"confidence": confidence}
        # })
        # print("DEBUG: AI message saved.")
        
        # # 4. Check confidence for escalation
        # if confidence < 0.6: # Configurable threshold
        #     self.ticket_service.create_ticket(
        #         tenant_id, 
        #         conversation_id, 
        #         "high", 
        #         f"Low confidence AI response ({confidence}). User asked: {content}"
        #     )
                
        return message, ai_message

    def list_messages(self, conversation_id: str) -> List[Message]:
        return self.repo.get_by_conversation(conversation_id)
