import os
import google.generativeai as genai
import re
import json
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('models/gemini-2.5-flash')


def classify_ticket(description):

    prompt = f"""
    Classify this support ticket.

    Choose:
    category → billing, technical, account, general
    priority → low, medium, high, critical

    Respond ONLY in JSON format like:
    {{
        "category": "billing",
        "priority": "high"
    }}

    Ticket description: {description}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text

        # Extract JSON from response using regex
        json_match = re.search(r'\{.*\}', text, re.DOTALL)

        if not json_match:
            return None, None

        json_text = json_match.group()
        data = json.loads(json_text)

        return data.get("category"), data.get("priority")

    except Exception as e:
        print("Gemini error:", e)
        return None, None
