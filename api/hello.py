def handler(request, response):
    return response.json({
        "message": "Hello from Vercel Python 🚀"
    })
from supabase import create_client
import json
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


def handler(request, response):
    try:
        method = request.method

        # ---------------- POST ----------------
        if method == "POST":
            body = request.json()
            action = body.get("action")

            # REGISTER
            if action == "register":
                supabase.table("users").insert({
                    "name": body["name"],
                    "email": body["email"],
                    "password": body["password"],
                    "role": body.get("role", "user")
                }).execute()

                return response.json({"message": "Registered Successfully"})

            # LOGIN
            if action == "login":
                res = supabase.table("users").select("*")\
                    .eq("email", body["email"])\
                    .eq("password", body["password"]).execute()

                if res.data:
                    return response.json({
                        "message": "Login Success",
                        "role": res.data[0]["role"]
                    })

                return response.json({"message": "Invalid"}, status=401)

            # COMPLAINT
            if action == "complaint":
                category = smart_category(body["description"])

                supabase.table("complaints").insert({
                    "user_email": body["email"],
                    "title": body["title"],
                    "description": body["description"],
                    "category": category,
                    "status": "Pending"
                }).execute()

                return response.json({"message": "Complaint Submitted"})

        # ---------------- GET ----------------
        if method == "GET":
            query = request.query

            start = query.get("start")
            end = query.get("end")
            ctype = query.get("type")
            download = query.get("download")

            q = supabase.table("complaints").select("*")

            if start and end:
                q = q.gte("created_at", start).lte("created_at", end)

            if ctype and ctype != "All":
                q = q.eq("category", ctype)

            res = q.execute()
            data = res.data

            # EXCEL DOWNLOAD
            if download == "excel":
                df = pd.DataFrame(data)
                output = BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)

                return response.send(
                    output.read(),
                    headers={
                        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        "Content-Disposition": "attachment; filename=complaints.xlsx"
                    }
                )

            return response.json(data)

        return response.json({"message": "Invalid Request"}, status=400)

    except Exception as e:
        return response.json({"error": str(e)}, status=500)
