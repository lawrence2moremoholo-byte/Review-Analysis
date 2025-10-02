# backend/ai_analysis.py
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_review(review_text):
    """
    Analyze a single review: return sentiment, category, and AI response.
    """
    prompt = f"""
Classify this customer review by sentiment (Positive, Negative, Neutral) 
and category (Billing, Network, Service, Fraud, Delivery, Other).
Output format: Sentiment, Category

Review: "{review_text}"
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        text = response.choices[0].message.content.strip()
        # parse into sentiment and category
        sentiment, category = text.split(",")
        return {
            "sentiment": sentiment.strip(),
            "category": category.strip(),
            "ai_response": text
        }
    except Exception as e:
        print("❌ Error analyzing review:", e)
        return {"sentiment": "Unknown", "category": "Other", "ai_response": ""}


