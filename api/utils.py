from supabase import create_client

SUPABASE_URL = "PASTE_YOUR_SUPABASE_URL"
SUPABASE_KEY = "PASTE_YOUR_SUPABASE_ANON_KEY"

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
