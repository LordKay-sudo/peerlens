from fastapi import APIRouter, HTTPException

from peerlens.core.exceptions import IdentifierError, IngestionError, PeerLensError, RAGError
from peerlens.models.schemas import AskRequest, AskResponse
from peerlens.services.rag.qa import ask_paper

router = APIRouter(prefix="/papers", tags=["rag"])


@router.post("/ask", response_model=AskResponse)
async def ask_about_paper(request: AskRequest) -> AskResponse:
    try:
        return await ask_paper(
            identifier=request.identifier,
            question=request.question,
            top_k=request.top_k,
        )
    except IdentifierError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except IngestionError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RAGError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except PeerLensError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
