from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs
from api.utils import supabase, smart_category, complaints_to_excel
import base64

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Submit complaint
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

        self.respond({"message":"Complaint Submitted"})

    def do_GET(self):
        # Admin: list/filter/download complaints
        query = parse_qs(self.path.split("?")[1]) if "?" in self.path else {}
        start_date = query.get("start_date", [None])[0]
        end_date = query.get("end_date", [None])[0]
        download = query.get("download", [None])[0]

        q = supabase.table("complaints").select("*")
        if start_date and end_date:
            q = q.gte("created_at", start_date).lte("created_at", end_date)
        res = q.execute()
        data = res.data

        if download == "excel":
            excel_bytes = complaints_to_excel(data)
            self.send_response(200)
            self.send_header("Content-Type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            self.send_header("Content-Disposition","attachment; filename=complaints.xlsx")
            self.end_headers()
            self.wfile.write(excel_bytes)
        else:
            self.respond(data)

    def respond(self,data,status=200):
        self.send_response(status)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
