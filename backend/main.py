from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from fastapi import FastAPI
from backend.routes import recon 
import sqlite3
import os

app = FastAPI()
app.include_router(recon.router)

# === Allow cross-origin for your app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "recon_reports.db"

# === Report schema
class ReconReport(BaseModel):
    id: int | None = None  # Auto-incremented
    location: str
    threat_level: str
    notes: str
    timestamp: str  # ISO format string


# === Database setup
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS recon_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            threat_level TEXT NOT NULL,
            notes TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# === Auto-delete logic
def delete_old_reports():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    cutoff = (datetime.utcnow() - timedelta(hours=24)).isoformat()
    c.execute("""
        DELETE FROM recon_reports
        WHERE threat_level != 'Critical' AND timestamp < ?
    """, (cutoff,))
    conn.commit()
    conn.close()


@app.on_event("startup")
def startup():
    init_db()
    delete_old_reports()


# === API Endpoints ===

@app.get("/recon", response_model=List[ReconReport])
def get_all_reports():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, location, threat_level, notes, timestamp FROM recon_reports ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return [ReconReport(id=row[0], location=row[1], threat_level=row[2], notes=row[3], timestamp=row[4]) for row in rows]


@app.post("/recon", response_model=ReconReport)
def submit_report(report: ReconReport):
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO recon_reports (location, threat_level, notes, timestamp)
        VALUES (?, ?, ?, ?)
    """, (report.location, report.threat_level, report.notes, now))
    conn.commit()
    report_id = c.lastrowid
    conn.close()
    return {**report.dict(), "id": report_id, "timestamp": now}


@app.delete("/recon/{report_id}")
def delete_report(report_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM recon_reports WHERE id = ?", (report_id,))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Deleted"}
