from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from supabase import create_client

# 🔐 SUPABASE CONFIG
SUPABASE_URL = "https://iawnianxqhimhtwzmmna.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlhd25pYW54cWhpbWh0d3ptbW5hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3MzM0ODYsImV4cCI6MjA4NjMwOTQ4Nn0.8MOrJYZECltksdN53KqeLSzu-bGNTvxSUT3fIDWgRtw"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class handler(BaseHTTPRequestHandler):

    # ---------- POST REQUESTS ----------
    def do_POST(self):
        path = self.path
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))

        # 🟢 REGISTER
        if path == "/api/register":
            supabase.table("users").insert({
                "name": body["name"],
                "email": body["email"],
                "password": body["password"],
                "role": body.get("role", "user")
            }).execute()

            return self.respond({"message": "Registered Successfully"})

        # 🟢 LOGIN
        if path == "/api/login":
            res = supabase.table("users").select("*")\
                .eq("email", body["email"])\
                .eq("password", body["password"])\
                .execute()

            if res.data:
                return self.respond({
                    "message": "Login Success",
                    "role": res.data[0]["role"]
                })
            else:
                return self.respond({"message": "Invalid Credentials"}, 401)

        # 🟢 SUBMIT COMPLAINT
        if path == "/api/complaint":
            supabase.table("complaints").insert({
                "user_email": body["email"],
                "title": body["title"],
                "description": body["description"],
                "type": body.get("type", "General"),
                "status": "Pending"
            }).execute()

            return self.respond({"message": "Complaint Submitted"})

    # ---------- GET REQUESTS ----------
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # 🟢 USER TRACK COMPLAINT
        if path == "/api/my-complaints":
            email = query.get("email", [None])[0]

            res = supabase.table("complaints")\
                .select("*")\
                .eq("user_email", email)\
                .execute()

            return self.respond(res.data)

        # 🟢 ADMIN VIEW ALL
        if path == "/api/admin/complaints":
            res = supabase.table("complaints").select("*").execute()
            return self.respond(res.data)

    # ---------- PUT REQUEST ----------
    def do_PUT(self):
        if self.path == "/api/admin/update":
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))

            supabase.table("complaints").update({
                "status": body["status"]
            }).eq("id", body["id"]).execute()

            return self.respond({"message": "Status Updated"})

    # ---------- RESPONSE ----------
    def respond(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
