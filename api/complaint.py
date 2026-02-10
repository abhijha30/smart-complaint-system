from http.server import BaseHTTPRequestHandler
import json
from api.utils import supabase, smart_category

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        category = smart_category(body["description"])

        supabase.table("complaints").insert({
            "user_email": body["email"],
            "title": body["title"],
            "description": body["description"],
            "category": category,
            "status": "Pending"
        }).execute()

        self.respond({"message": "Complaint Submitted"})

    def do_GET(self):
        # ADMIN VIEW
        data = supabase.table("complaints").select("*").execute()
        self.respond(data.data)

    def respond(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
