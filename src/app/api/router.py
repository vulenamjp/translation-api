# src/app/api/router.py
from fastapi import APIRouter
from app.api.endpoints import translation

api_router = APIRouter()

api_router.include_router(translation.router, prefix="/translation", tags=["Translation"])