import openai
from backend.config import OPENAI_API_KEY
from backend.database import update_review

openai.api_key = "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"

def analyze_review(review_text, review_id=None):
    """Use OpenAI to analyze sentiment & category of a review."""
    prompt = f"""
    Analyze this customer review. 
    1. Sentiment: Positive, Negative, or Neutral.
    2. Category: Billing, Network, Service, Fraud, Delivery, Other.
    
    Review: "{review_text}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a review analysis AI."},
                  {"role": "user", "content": prompt}]
    )

    result_text = response["choices"][0]["message"]["content"].strip()

    # Simple parsing (you can improve this with regex/structured output)
    sentiment = "Neutral"
    category = "Other"

    if "Positive" in result_text:
        sentiment = "Positive"
    elif "Negative" in result_text:
        sentiment = "Negative"

    for cat in ["Billing", "Network", "Service", "Fraud", "Delivery"]:
        if cat.lower() in result_text.lower():
            category = cat
            break

    # Update DB if review_id given
    if review_id:
        update_review(review_id, sentiment, category)

    return {"sentiment": sentiment, "category": category}
