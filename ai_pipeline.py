import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_document_text(text_content):
    """
    Takes raw OCR/document text and returns structured summary, 
    Tanglish explanation, Tamil explanation, and actionable steps.
    """
    prompt = f"""
    You are Sahaaya AI, a digital inclusion assistant helping non-technical users in South India.
    Analyze the following extracted document text and break it down simply.

    Document Text:
    \"\"\"{text_content}\"\"\"

    Respond ONLY in valid JSON format with the following keys:
    {{
      "doc_type": "Brief classification (e.g., Utility Bill, Government Notice, Application Form, Bank Message)",
      "urgency": "High / Medium / Low",
      "key_details": [
        "Detail 1 (e.g., Amount Due)",
        "Detail 2 (e.g., Due Date)",
        "Detail 3 (e.g., Account / Application ID)"
      ],
      "tanglish_summary": "Conversational Tanglish (Tamil written in English script) explanation of what this document means, why it matters, and what happens if ignored.",
      "tamil_summary": "Clear, simple Tamil explanation in Tamil script.",
      "english_summary": "Simple, non-jargon English summary.",
      "action_steps": [
        "Step 1: What to do first",
        "Step 2: Where to pay/submit",
        "Step 3: What to keep safe"
      ]
    }}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {
            "doc_type": "Unknown Document",
            "urgency": "Medium",
            "key_details": ["Error processing AI response"],
            "tanglish_summary": "Apologies, AI pipeline process panna mudiyala. Technical error wandhurukku.",
            "tamil_summary": "மன்னிக்கவும், செயலாக்குவதில் பிழை ஏற்பட்டுள்ளது.",
            "english_summary": "Failed to process document with AI.",
            "action_steps": ["Please try again with a clearer image or text input."]
        }

if __name__ == "__main__":
    # Test run
    sample_text = "TNEB Notice. Account No: 09-214-884-12. Bill Amount: Rs 2450. Due Date: 20-Aug-2026. Disconnection warning if not paid."
    result = analyze_document_text(sample_text)
    print(json.dumps(result, indent=2, ensure_ascii=False))