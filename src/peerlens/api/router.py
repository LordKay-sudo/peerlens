from fastapi import APIRouter

from peerlens.api.routes import ask, health, papers

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(papers.router)
api_router.include_router(ask.router)
