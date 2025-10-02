from openai import OpenAI
from backend.config import OPENAI_API_KEY

client = OpenAI(api_key="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")

def analyze_review(review_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": review_text}
        ]
    )
    return response.choices[0].message.content


def analyze_review(review_text, review_id=None):
    """
    Analyze sentiment and category of a review using OpenAI.
    If review_id is provided, update the database.
    """
    prompt = f"""
    Analyze this customer review. 
    1. Sentiment: Positive, Negative, or Neutral.
    2. Category: Billing, Network, Service, Fraud, Delivery, Other.
    
    Review: "{review_text}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a customer review analysis AI."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response["choices"][0]["message"]["content"].strip()

    # Basic parsing
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

    if review_id:
        update_review(review_id, sentiment, category)

    return {"sentiment": sentiment, "category": category}
