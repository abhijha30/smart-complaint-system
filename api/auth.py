from http.server import BaseHTTPRequestHandler
import json
from api.utils import supabase

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        email = body["email"]
        password = body["password"]
        action = body["action"]  # login / register

        if action == "register":
            role = body.get("role", "user")
            supabase.table("users").insert({
                "name": body["name"],
                "email": email,
                "password": password,
                "role": role
            }).execute()

            self.respond({"message": "Registered Successfully"})

        elif action == "login":
            res = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
            if res.data:
                self.respond({"message": "Login Success", "role": res.data[0]["role"]})
            else:
                self.respond({"message": "Invalid Credentials"}, 401)

    def respond(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
