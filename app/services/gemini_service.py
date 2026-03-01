import google.generativeai as genai
from app.config import GEMINI_API_KEY
from fastapi import HTTPException

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_text(prompt: str):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "429" in error_msg:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please check your API key and billing."
            )
        elif "api key" in error_msg.lower():
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key. Please check your configuration."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Gemini API error: {error_msg}"
            )