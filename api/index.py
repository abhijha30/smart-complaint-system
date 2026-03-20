from supabase import create_client
import json

SUPABASE_URL = "https://pdvotajkxpoyovqgggtq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBkdm90YWpreHBveW92cWdnZ3RxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM5ODkzNDgsImV4cCI6MjA4OTU2NTM0OH0.lju-IlKeTbhn6D5jfZh08ePS7s32t1OBFGivt0ZNPpA"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def handler(request):
    try:
        # -------- GET REQUESTS --------
        if request.method == "GET":

            # TRACK COMPLAINT
            if request.path.startswith("/api/track"):
                cid = request.query.get("id")
                res = supabase.table("complaints").select("*").eq("id", cid).execute()

                return {
                    "statusCode": 200,
                    "body": json.dumps(res.data)
                }

            # ADMIN VIEW
            if request.path.startswith("/api/admin"):
                res = supabase.table("complaints").select("*").execute()

                return {
                    "statusCode": 200,
                    "body": json.dumps(res.data)
                }

        # -------- POST REQUESTS --------
        if request.method == "POST":
            body = json.loads(request.body)

            # REGISTER
            if request.path == "/api/register":
                supabase.table("users").insert({
                    "name": body["name"],
                    "email": body["email"],
                    "password": body["password"],
                    "role": body.get("role", "user")
                }).execute()

                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Registered"})
                }

            # LOGIN
            if request.path == "/api/login":
                res = supabase.table("users").select("*")\
                    .eq("email", body["email"])\
                    .eq("password", body["password"]).execute()

                if res.data:
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message": "Login Success",
                            "role": res.data[0]["role"]
                        })
                    }

                return {
                    "statusCode": 401,
                    "body": json.dumps({"message": "Invalid"})
                }

            # SUBMIT COMPLAINT
            if request.path == "/api/complaint":
                res = supabase.table("complaints").insert({
                    "name": body["name"],
                    "user_email": body["email"],
                    "contact": body["contact"],
                    "title": body["title"],
                    "description": body["remark"],
                    "type": body["type"],
                    "status": "Pending"
                }).execute()

                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Complaint Submitted"})
                }

        # -------- PUT REQUEST --------
        if request.method == "PUT":
            body = json.loads(request.body)

            if request.path == "/api/update":
                supabase.table("complaints").update({
                    "status": body["status"]
                }).eq("id", body["id"]).execute()

                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": "Updated"})
                }

        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Not Found"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
