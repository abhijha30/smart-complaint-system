from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from supabase import create_client
from pydantic import BaseModel
from datetime import date
import pandas as pd
from io import BytesIO
import secrets

SUPABASE_URL = "PASTE_YOUR_SUPABASE_URL"
SUPABASE_KEY = "PASTE_YOUR_SUPABASE_ANON_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def admin_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct = secrets.compare_digest(credentials.username, ADMIN_USER) and \
              secrets.compare_digest(credentials.password, ADMIN_PASS)
    if not correct:
        raise HTTPException(status_code=401, detail="Unauthorized")

class Complaint(BaseModel):
    name: str
    age: int
    email: str
    contact: str
    designation: str
    company: str | None = ""
    complaint: str

@app.get("/")
def root():
    return {"status": "Smart Complaint System API Running"}

@app.post("/submit")
def submit_complaint(data: Complaint):
    response = supabase.table("complaints").insert(data.dict()).execute()

    if response.data is None:
        raise HTTPException(status_code=500, detail="Database insert failed")

    return {
        "success": True,
        "message": "Complaint submitted successfully"
    }


@app.get("/admin/complaints", dependencies=[Depends(admin_auth)])
def get_complaints(from_date: date | None = None, to_date: date | None = None):
    query = supabase.table("complaints").select("*")
    if from_date:
        query = query.gte("created_at", str(from_date))
    if to_date:
        query = query.lte("created_at", str(to_date))
    return query.execute().data

@app.get("/admin/download", dependencies=[Depends(admin_auth)])
def download_excel():
    data = supabase.table("complaints").select("*").execute().data
    df = pd.DataFrame(data)
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer.getvalue()
