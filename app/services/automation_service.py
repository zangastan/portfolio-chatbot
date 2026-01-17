from app.core.config import settings
from app.services.knowledge_service import KnowledgeService
import google.generativeai as genai
import json
from typing import List ,Dict
import os

class AutomationService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.knowledge_service = KnowledgeService()

    async def generate_response(self, user_message: str) -> dict:
        """
        Generates a response using Gemini based on full-text context.
        """
        print("CWD:", os.getcwd())


        # # 1. Retrieve all relevant context (full document text for the tenant)
        # context = self.knowledge_service.search_context(tenant_id, user_message)
        # print({"history": HistoryConvo})

        # 2. Construct the prompt
        system_instruction = (
            """
            "You are Augustine Kasolota's personal assistant.
            Answer questions about Augustine—his skills, education, interests, passions, hobbies, life, and general information about him.
            Keep responses friendly, light, and sometimes playful.
            Short answers are fine.
            If unsure, respond thoughtfully instead of saying "I don’t know'
            """
        )
        with open("app/services/augustine.txt", "r") as f:
            context = f.read()
        
        full_prompt = (
            f"{system_instruction}\n\n"
            f"Context:\n{context}\n\n"
            f"User Question: {user_message}"
        )

        try:
            # Using flash for speed and cost efficiency
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.5,
                    max_output_tokens=500,
                    response_mime_type="application/json"
                )
            )

            text = response.text.strip()

            # Clean code fences if model adds them (though response_mime_type should prevent this)
            if text.startswith("```"):
                text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:].strip()

            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {
                    "response": text,
                    "confidence": 0.5
                }

        except Exception as e:
            print(f"DEBUG: AI Generation Error: {e}")
            return {
                "response": "I am currently unable to process your request. Please try again later.",
                "confidence": 0.0
            }
