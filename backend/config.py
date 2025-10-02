import os

# Load from environment (set these in Render → Environment Variables)
SUPABASE_URL = os.getenv("https://zgennqckgzokxnfwpsxh.supabase.co")
SUPABASE_KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpnZW5ucWNrZ3pva3huZndwc3hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNzcyMDMsImV4cCI6MjA3NDk1MzIwM30.HAou28iXuAGgGg6gqJF4AowNtSJjNOoBsHqFi6OAURc")
OPENAI_API_KEY = os.getenv("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")

# Safety check (optional, helps debug on Render)
if not SUPABASE_URL or not SUPABASE_KEY or not OPENAI_API_KEY:
    raise ValueError("❌ Missing environment variables. Check Render settings.")
