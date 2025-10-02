from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_review(review_data: dict):
    supabase.table("reviews").insert(review_data).execute()

def update_review(review_id, update_data: dict):
    supabase.table("reviews").update(update_data).eq("id", review_id).execute()

def get_all_reviews():
    return supabase.table("reviews").select("*").execute().data

