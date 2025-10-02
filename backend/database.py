from supabase import create_client
from backend.config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client("https://zgennqckgzokxnfwpsxh.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpnZW5ucWNrZ3pva3huZndwc3hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNzcyMDMsImV4cCI6MjA3NDk1MzIwM30.HAou28iXuAGgGg6gqJF4AowNtSJjNOoBsHqFi6OAURc")

def get_all_reviews():
    """Fetch all reviews from the database."""
    response = supabase.table("reviews").select("*").execute()
    return response.data or []

def add_review(review, sentiment, category, ai_response=""):
    data = {
        "review": review,
        "sentiment": sentiment,
        "category": category,
        "ai_response": ai_response
    }
    supabase.table("reviews").insert(data).execute()

def update_review(review_id, sentiment, category):
    """Update analysis results for a review."""
    supabase.table("reviews").update({
        "sentiment": sentiment,
        "category": category
    }).eq("id", review_id).execute()
