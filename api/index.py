from supabase import create_client
import json

SUPABASE_URL = "https://pdvotajkxpoyovqgggtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkdm90YWpreHBveW92cWdnZ3RxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5ODkzNDgsImV4cCI6MjA4OTU2NTM0OH0.lju-IlKeTbhn6D5jfZh08ePS7s32t1OBFGivt0ZNPpA"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def handler(request, response):
    try:
        path = request.path
        method = request.method

        # -------- GET --------
        if method == "GET":

            if path.startswith("/api/track"):
                cid = request.query.get("id")
                res = supabase.table("complaints").select("*").eq("id", cid).execute()
                return response.json(res.data)

            if path.startswith("/api/admin"):
                res = supabase.table("complaints").select("*").execute()
                return response.json(res.data)

        # -------- POST --------
        if method == "POST":
            body = request.json()

            if path == "/api/register":
                supabase.table("users").insert(body).execute()
                return response.json({"message": "Registered"})

            if path == "/api/login":
                res = supabase.table("users").select("*")\
                    .eq("email", body["email"])\
                    .eq("password", body["password"]).execute()

                if res.data:
                    return response.json({
                        "message": "Login Success",
                        "role": res.data[0]["role"]
                    })

                return response.json({"message": "Invalid"}, status=401)

            if path == "/api/complaint":
                supabase.table("complaints").insert({
                    "name": body["name"],
                    "user_email": body["email"],
                    "contact": body["contact"],
                    "title": body["title"],
                    "description": body["remark"],
                    "type": body["type"],
                    "status": "Pending"
                }).execute()

                return response.json({"message": "Submitted"})

        # -------- PUT --------
        if method == "PUT":
            body = request.json()

            if path == "/api/update":
                supabase.table("complaints").update({
                    "status": body["status"]
                }).eq("id", body["id"]).execute()

                return response.json({"message": "Updated"})

        return response.json({"message": "Not Found"}, status=404)

    except Exception as e:
        return response.json({"error": str(e)}, status=500)
