import openai
from config import OPENAI_API_KEY
from database import update_review

openai.api_key = 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

CATEGORIES = ["billing","network","service","fraud","delivery"]

def analyze_review(review_id, text):
    prompt = f"""
    Categorize the following review into one of {CATEGORIES} and determine sentiment (positive, negative, neutral). 
    Review: \"{text}\"
    Respond ONLY in JSON format: {{"category": "category_here", "sentiment": "sentiment_here"}}
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0
    )
    import json
    try:
        result = json.loads(response['choices'][0]['message']['content'])
    except:
        result = {"category":"unknown","sentiment":"neutral"}
    update_review(review_id, result)
    return result

