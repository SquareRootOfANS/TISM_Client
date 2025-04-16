# backend/routes/recon.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

# Pydantic model
class ReconReport(BaseModel):
    id: int
    location: str
    description: str
    threat_level: str
    timestamp: datetime

# Simulated storage
reports_db: List[ReconReport] = []

# GET all reports
@router.get("/recon", response_model=List[ReconReport])
def get_reports():
    return reports_db

# POST a new report
@router.post("/recon", response_model=ReconReport)
def add_report(report: ReconReport):
    reports_db.append(report)
    return report

# DELETE a report by ID
@router.delete("/recon/{report_id}")
def delete_report(report_id: int):
    global reports_db
    reports_db = [r for r in reports_db if r.id != report_id]
    return {"message": "Report deleted"}
