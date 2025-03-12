# src/app/api/dependencies.py
from app.services.translation_service import translator_service

def get_translator_service():
    return translator_service