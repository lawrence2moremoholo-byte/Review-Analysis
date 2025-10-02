# backend/ai_analysis.py

import os
from openai import OpenAI

from backend.config import OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_review(review_text: str) -> dict:
    """
    Analyze a customer review using OpenAI:
    - Sentiment: Positive, Negative, Neutral
    - Category: Billing, Network, Service, Fraud, Delivery, Other
    - AI Response: Suggested reply for company
    """

    prompt = f"""
    You are an AI assistant for customer review analysis.
    Analyze the following customer review:

    "{review_text}"

    1. Determine the sentiment: Positive, Negative, or Neutral.
    2. Determine the category: Billing, Network, Service, Fraud, Delivery, or Other.
    3. Suggest a professional response for the company.

    Respond in JSON format exactly like this:
    {{
        "sentiment": "<Positive/Negative/Neutral>",
        "category": "<Billing/Network/Service/Fraud/Delivery/Other>",
        "ai_response": "<Suggested response>"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        # Extract AI output
        content = response.choices[0].message.content.strip()

        # Parse as dict
        import json
        analysis = json.loads(content)
        return analysis

    except Exception as e:
        print(f"❌ Error analyzing review: {e}")
        return {
            "sentiment": "Unknown",
            "category": "Other",
            "ai_response": ""
        }

