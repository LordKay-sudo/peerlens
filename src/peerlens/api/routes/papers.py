from fastapi import APIRouter, HTTPException

from peerlens.core.exceptions import IdentifierError, IngestionError, PeerLensError
from peerlens.models.schemas import AnalyzeRequest, QualityReport
from peerlens.services.reports import analyze_paper

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
