from http.server import BaseHTTPRequestHandler
import json
from supabase import create_client
from urllib.parse import urlparse, parse_qs
import pandas as pd
from io import BytesIO

SUPABASE_URL = "https://iawnianxqhimhtwzmmna.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkdm90YWpreHBveW92cWdnZ3RxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5ODkzNDgsImV4cCI6MjA4OTU2NTM0OH0.lju-IlKeTbhn6D5jfZh08ePS7s32t1OBFGivt0ZNPpA"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def smart_category(text):
    text = text.lower()
    if "electric" in text:
        return "Electricity"
    if "water" in text:
        return "Water"
    if "wifi" in text:
        return "IT"
    return "General"

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        action = body.get("action")

        # 🔐 REGISTER
        if action == "register":
            supabase.table("users").insert({
                "name": body["name"],
                "email": body["email"],
                "password": body["password"],
                "role": body.get("role", "user")
            }).execute()

            return self.respond({"message": "Registered Successfully"})

        # 🔑 LOGIN
        if action == "login":
            res = supabase.table("users").select("*") \
                .eq("email", body["email"]) \
                .eq("password", body["password"]) \
                .execute()

            if res.data:
                return self.respond({
                    "message": "Login Success",
                    "role": res.data[0]["role"]
                })

            return self.respond({"message": "Invalid"}, 401)

        # 📝 SUBMIT COMPLAINT
        if action == "complaint":
            category = smart_category(body["description"])

            supabase.table("complaints").insert({
                "user_email": body["email"],
                "title": body["title"],
                "description": body["description"],
                "category": category,
                "status": "Pending"
            }).execute()

            return self.respond({"message": "Complaint Submitted"})

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        start = query.get("start", [None])[0]
        end = query.get("end", [None])[0]
        ctype = query.get("type", [None])[0]
        download = query.get("download", [None])[0]

        q = supabase.table("complaints").select("*")

        # 📅 FILTER BY DATE
        if start and end:
            q = q.gte("created_at", start).lte("created_at", end)

        # 📂 FILTER BY TYPE
        if ctype and ctype != "All":
            q = q.eq("category", ctype)

        res = q.execute()
        data = res.data

        # 📥 EXCEL DOWNLOAD
        if download == "excel":
            df = pd.DataFrame(data)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition", "attachment; filename=complaints.xlsx")
            self.end_headers()
            self.wfile.write(output.read())
            return

        return self.respond(data)

    def respond(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
