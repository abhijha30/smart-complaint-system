from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from supabase import create_client
import smtplib
from email.mime.text import MIMEText

# 🔐 SUPABASE
SUPABASE_URL = "https://pdvotajkxpoyovqgggtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkdm90YWpreHBveW92cWdnZ3RxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5ODkzNDgsImV4cCI6MjA4OTU2NTM0OH0.lju-IlKeTbhn6D5jfZh08ePS7s32t1OBFGivt0ZNPpA"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 📧 EMAIL FUNCTION
def send_email(to_email, complaint_id):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    track_link = f"https://your-project.vercel.app/frontend/track.html?id={complaint_id}"

    body = f"""
Thank you for submitting your complaint.

Please have some patience, we are working on it.

Track your complaint:
{track_link}
"""

    msg = MIMEText(body)
    msg["Subject"] = "Complaint Registered"
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        path = self.path
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))

        # REGISTER
        if path == "/api/register":
            supabase.table("users").insert({
                "name": body["name"],
                "email": body["email"],
                "password": body["password"],
                "role": body.get("role", "user")
            }).execute()

            return self.respond({"message": "Registered"})

        # LOGIN
        if path == "/api/login":
            res = supabase.table("users").select("*")\
                .eq("email", body["email"])\
                .eq("password", body["password"]).execute()

            if res.data:
                return self.respond({
                    "message": "Login Success",
                    "role": res.data[0]["role"]
                })
            return self.respond({"message": "Invalid"}, 401)

        # SUBMIT COMPLAINT
        if path == "/api/complaint":
            res = supabase.table("complaints").insert({
                "name": body["name"],
                "user_email": body["email"],
                "contact": body["contact"],
                "title": body["title"],
                "description": body["remark"],
                "type": body["type"],
                "status": "Pending"
            }).execute()

            cid = res.data[0]["id"]
            send_email(body["email"], cid)

            return self.respond({"message": "Complaint Submitted"})

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # USER TRACK BY ID
        if path == "/api/track":
            cid = query.get("id", [None])[0]
            res = supabase.table("complaints").select("*").eq("id", cid).execute()
            return self.respond(res.data)

        # USER VIEW THEIR COMPLAINTS
        if path == "/api/my":
            email = query.get("email", [None])[0]
            res = supabase.table("complaints").select("*").eq("user_email", email).execute()
            return self.respond(res.data)

        # ADMIN VIEW ALL
        if path == "/api/admin":
            res = supabase.table("complaints").select("*").execute()
            return self.respond(res.data)

    def do_PUT(self):
        if self.path == "/api/update":
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))

            supabase.table("complaints").update({
                "status": body["status"]
            }).eq("id", body["id"]).execute()

            return self.respond({"message": "Updated"})

    def respond(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
