from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from supabase import create_client, Client
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse

# -------------------- Supabase Setup --------------------
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------- Admin Credentials --------------------
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

security = HTTPBasic()
app = FastAPI()

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Submit Complaint --------------------
@app.post("/submit")
async def submit_complaint(request: Request):
    try:
        data = await request.json()
        name = data.get("name")
        email = data.get("email")
        complaint = data.get("complaint")
        if not all([name, email, complaint]):
            raise HTTPException(status_code=400, detail="All fields are required")

        supabase.table("complaints").insert({
            "name": name,
            "email": email,
            "complaint": complaint
        }).execute()

        return {"status": "success", "message": "Complaint submitted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# -------------------- Admin Authentication --------------------
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == ADMIN_USER and credentials.password == ADMIN_PASS):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# -------------------- Get Complaints --------------------
@app.get("/admin/complaints")
async def get_complaints(start: str = None, end: str = None, auth: bool = Depends(verify_admin)):
    query = supabase.table("complaints").select("*")
    if start:
        query = query.gte("created_at", start)
    if end:
        query = query.lte("created_at", end)
    res = query.execute()
    return {"data": res.data}

# -------------------- Download Excel --------------------
@app.get("/admin/download")
async def download_excel(start: str = None, end: str = None, auth: bool = Depends(verify_admin)):
    query = supabase.table("complaints").select("*")
    if start:
        query = query.gte("created_at", start)
    if end:
        query = query.lte("created_at", end)
    res = query.execute()
    df = pd.DataFrame(res.data)
    if df.empty:
        df = pd.DataFrame(columns=["id", "name", "email", "complaint", "created_at"])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=complaints.xlsx"}
    )

# -------------------- Local Testing --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
