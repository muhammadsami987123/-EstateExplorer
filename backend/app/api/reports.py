from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from app.schemas.report import ReportGenerateRequest
from app.services.reports import generate_report, generate_pdf, generate_markdown, generate_text
from app.json_db import JsonDB

router = APIRouter()


@router.post("/generate")
async def create_report(request: ReportGenerateRequest):
    """Generate a full property & market intelligence report."""
    preferences = request.preferences.model_dump()
    report = await generate_report(preferences)
    return report


@router.get("")
async def list_reports():
    """List all previously generated reports (summaries only)."""
    reports = JsonDB.load('reports')
    summaries = []
    for r in reports:
        summaries.append({
            "id": r.get("id"),
            "created_at": r.get("created_at"),
            "preferences": r.get("preferences"),
            "total_matches": r.get("total_matches"),
            "data_type": r.get("data_type")
        })
    summaries.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return {"reports": summaries, "total": len(summaries)}


@router.get("/{report_id}")
async def get_report(report_id: str):
    """Get a full report by ID."""
    report = JsonDB.find_one('reports', report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/{report_id}/download")
async def download_report(report_id: str, format: str = Query("pdf")):
    """Download a report in pdf, markdown, or text format.
    
    Frontend calls: /reports/{id}/download?format=pdf|markdown|text
    """
    report = JsonDB.find_one('reports', report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    slug = report_id[:8]

    if format == "pdf":
        pdf_bytes = generate_pdf(report)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="report-{slug}.pdf"'}
        )
    elif format == "markdown":
        md = generate_markdown(report)
        return Response(
            content=md.encode("utf-8"),
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="report-{slug}.md"'}
        )
    elif format == "text":
        txt = generate_text(report)
        return Response(
            content=txt.encode("utf-8"),
            media_type="text/plain",
            headers={"Content-Disposition": f'attachment; filename="report-{slug}.txt"'}
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}. Use pdf, markdown, or text.")


@router.delete("/{report_id}")
async def delete_report(report_id: str):
    """Delete a report by ID."""
    success = JsonDB.delete('reports', report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"success": True, "message": "Report deleted"}
