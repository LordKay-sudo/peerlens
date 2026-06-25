from fastapi import APIRouter, File, HTTPException, UploadFile

from peerlens.core.exceptions import IdentifierError, IngestionError, PeerLensError
from peerlens.models.schemas import AnalyzeRequest, QualityReport
from peerlens.services.reports import analyze_paper, analyze_uploaded_pdf

router = APIRouter(prefix="/papers", tags=["papers"])


@router.post("/analyze", response_model=QualityReport)
async def analyze(request: AnalyzeRequest) -> QualityReport:
    try:
        return await analyze_paper(request.identifier)
    except IdentifierError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IngestionError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PeerLensError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/analyze/upload", response_model=QualityReport)
async def analyze_upload(file: UploadFile = File(...)) -> QualityReport:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Upload must be a .pdf file")

    try:
        content = await file.read()
        return await analyze_uploaded_pdf(file.filename, content)
    except IngestionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except PeerLensError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/analyze/{identifier:path}", response_model=QualityReport)
async def analyze_get(identifier: str) -> QualityReport:
    try:
        return await analyze_paper(identifier)
    except IdentifierError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IngestionError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PeerLensError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
