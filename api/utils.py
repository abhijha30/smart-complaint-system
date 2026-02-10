from supabase import create_client

SUPABASE_URL = "https://iawnianxqhimhtwzmmna.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlhd25pYW54cWhpbWh0d3ptbW5hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3MzM0ODYsImV4cCI6MjA4NjMwOTQ4Nn0.8MOrJYZECltksdN53KqeLSzu-bGNTvxSUT3fIDWgRtw"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def smart_category(text):
    text = text.lower()
    if "electric" in text or "power" in text:
        return "Electricity"
    if "water" in text:
        return "Water"
    if "wifi" in text or "internet" in text:
        return "IT"
    return "General"
