"""Export and Report Generation API Routes for PDF and CSV."""

import json
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.gap_analysis import SavedGapAnalysis
from app.models.roadmap import SavedRoadmap
from app.services.report_generator import (
    generate_gap_csv,
    generate_gap_pdf,
    generate_roadmap_csv,
    generate_roadmap_pdf,
)

router = APIRouter(prefix="/reports", tags=["Reports & Exports"])


@router.get("/gap-pdf")
def export_gap_pdf(analysis_id: str = Query(...), db: Session = Depends(get_db)):
    """Generate and stream a professional PDF report for a skill gap analysis."""
    rec = db.query(SavedGapAnalysis).filter(SavedGapAnalysis.id == analysis_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Gap analysis record not found.")

    gap_data = json.loads(rec.result_json)
    pdf_bytes = generate_gap_pdf(
        gap_data=gap_data,
        candidate_name=rec.candidate_name or "Candidate",
        job_title=rec.job_title or "Target Role"
    )

    filename = f"skillsync-gap-report-{analysis_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.get("/gap-csv")
def export_gap_csv(analysis_id: str = Query(...), db: Session = Depends(get_db)):
    """Generate and stream an RFC 4180 CSV export for a skill gap analysis."""
    rec = db.query(SavedGapAnalysis).filter(SavedGapAnalysis.id == analysis_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Gap analysis record not found.")

    gap_data = json.loads(rec.result_json)
    csv_bytes = generate_gap_csv(
        gap_data=gap_data,
        candidate_name=rec.candidate_name or "Candidate",
        job_title=rec.job_title or "Target Role"
    )

    filename = f"skillsync-gap-report-{analysis_id}.csv"
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.get("/roadmap-pdf")
def export_roadmap_pdf(roadmap_id: str = Query(...), db: Session = Depends(get_db)):
    """Generate and stream a professional PDF document for a learning roadmap."""
    rec = db.query(SavedRoadmap).filter(SavedRoadmap.id == roadmap_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Roadmap not found.")

    roadmap_data = json.loads(rec.roadmap_json)
    pdf_bytes = generate_roadmap_pdf(roadmap_data)

    filename = f"skillsync-learning-roadmap-{roadmap_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.get("/roadmap-csv")
def export_roadmap_csv(roadmap_id: str = Query(...), db: Session = Depends(get_db)):
    """Generate and stream a structured CSV export for a learning roadmap."""
    rec = db.query(SavedRoadmap).filter(SavedRoadmap.id == roadmap_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Roadmap not found.")

    roadmap_data = json.loads(rec.roadmap_json)
    csv_bytes = generate_roadmap_csv(roadmap_data)

    filename = f"skillsync-learning-roadmap-{roadmap_id}.csv"
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )
