from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pandas as pd
from supabase import create_client, Client
from datetime import datetime
from io import BytesIO
from fastapi.responses import StreamingResponse

# Supabase config
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "password123"

security = HTTPBasic()

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace "*" with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Submit complaint
@app.post("/submit")
async def submit_complaint(request: Request):
    data = await request.json()
    name = data.get("name")
    email = data.get("email")
    complaint = data.get("complaint")
    if not all([name, email, complaint]):
        raise HTTPException(status_code=400, detail="Missing fields")
    
    supabase.table("complaints").insert({
        "name": name,
        "email": email,
        "complaint": complaint
    }).execute()
    
    return {"status": "success", "message": "Complaint submitted successfully"}

# Admin authentication
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if not (credentials.username == ADMIN_USER and credentials.password == ADMIN_PASS):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# Get complaints (with optional date filter)
@app.get("/admin/complaints")
async def get_complaints(start: str = None, end: str = None, auth: bool = Depends(verify_admin)):
    query = supabase.table("complaints").select("*")
    if start:
        query = query.gte("created_at", start)
    if end:
        query = query.lte("created_at", end)
    res = query.execute()
    return {"data": res.data}

# Download Excel
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
