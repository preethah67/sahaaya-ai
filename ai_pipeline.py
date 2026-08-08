import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_TEMPLATE = """
You are Sahaaya AI, a digital inclusion assistant helping non-technical users in South India.
Analyze the provided document (text or image) and break it down simply.

Respond ONLY in valid JSON format with the following keys:
{
  "doc_type": "Brief classification (e.g., Utility Bill, Government Notice, Application Form)",
  "urgency": "High / Medium / Low",
  "key_details": [
    "Detail 1 (e.g., Amount Due)",
    "Detail 2 (e.g., Due Date)",
    "Detail 3 (e.g., Account / ID)"
  ],
  "tanglish_summary": "Conversational Tanglish (Tamil written in English script) explanation of what this document means.",
  "tamil_summary": "Clear, simple Tamil explanation in Tamil script.",
  "english_summary": "Simple, non-jargon English summary.",
  "action_steps": [
    "Step 1: What to do first",
    "Step 2: Where to pay/submit",
    "Step 3: What to keep safe"
  ]
}
"""

def analyze_document(text_content=None, image_path=None):
    """
    Analyzes document text or image using Gemini Vision / Gemini API.
    """
    try:
        contents = []
        if image_path:
            img = Image.open(image_path)
            contents.append(img)
            contents.append("Extract and analyze all readable text from this document image.")
        elif text_content:
            contents.append(f"Document Text:\n\"\"\"{text_content}\"\"\"")
        else:
            raise ValueError("Neither text nor image was provided.")

        contents.append(PROMPT_TEMPLATE)

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {
            "doc_type": "Error",
            "urgency": "Medium",
            "key_details": ["Processing failed"],
            "tanglish_summary": "Apologies, process panna mudiyala. Clear image upload pannunga.",
            "tamil_summary": "செயலாக்குவதில் பிழை ஏற்பட்டது. தெளிவான படத்தை பதிவேற்றவும்.",
            "english_summary": "Could not process document image.",
            "action_steps": ["Please upload a clearer image or enter text manually."]
        }