from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Create client using ENV vars (not hardcoded strings)
supabase = create_client(https://zgennqckgzokxnfwpsxh.supabase.co, eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpnZW5ucWNrZ3pva3huZndwc3hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNzcyMDMsImV4cCI6MjA3NDk1MzIwM30.HAou28iXuAGgGg6gqJF4AowNtSJjNOoBsHqFi6OAURc)

def insert_review(review_data: dict):
    supabase.table("reviews").insert(review_data).execute()

def update_review(review_id, update_data: dict):
    supabase.table("reviews").update(update_data).eq("id", review_id).execute()

def get_all_reviews():
    return supabase.table("reviews").select("*").execute().data
