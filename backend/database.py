# backend/database.py
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client("https://zgennqckgzokxnfwpsxh.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpnZW5ucWNrZ3pva3huZndwc3hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNzcyMDMsImV4cCI6MjA3NDk1MzIwM30.HAou28iXuAGgGg6gqJF4AowNtSJjNOoBsHqFi6OAURc")

def get_all_reviews():
    response = supabase.table("reviews").select("*").execute()
    if response.data:
        return response.data
    return []

def add_review(review, sentiment, category, ai_response=""):
    """
    Insert a review into Supabase.
    """
    data = {
        "review": review,
        "sentiment": sentiment,
        "category": category,
        "ai_response": ai_response
    }
    supabase.table("reviews").insert(data).execute()

