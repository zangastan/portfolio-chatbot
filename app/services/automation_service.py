from app.core.config import settings
import google.generativeai as genai
import json
import os

class AutomationService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_response(self, user_message: str) -> dict:
        """
        Generates a response using Gemini based on Augustine's knowledge base.
        """
        system_instruction = (
            "You are Augustine Kasolota's personal assistant. "
            "Answer questions about Augustine—his skills, education, projects, and background—using the provided context. "
            "Keep responses friendly, professional, and concise. "
            "If the information is not in the context, respond politely based on what you know about him being a Computer Engineering student. "
            "Always return the response in JSON format with 'response' and 'confidence' keys."
        )
        
        context_path = os.path.join("app", "services", "augustine.txt")
        try:
            with open(context_path, "r") as f:
                context = f.read()
        except FileNotFoundError:
            context = "Information about Augustine is currently unavailable."
        
        full_prompt = (
            f"{system_instruction}\n\n"
            f"Context:\n{context}\n\n"
            f"User Question: {user_message}"
        )

        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    # max_output_tokens=500,
                    response_mime_type="application/json"
                )
            )

            text = response.text.strip()
            
            # Basic cleaning (though response_mime_type should handle it)
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
                "response": "I'm sorry, I'm having trouble connecting to my brain right now. Please try again later!",
                "confidence": 0.0
            }
