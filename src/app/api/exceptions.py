# src/app/api/exceptions.py
from fastapi import HTTPException

def translation_exception_handler(detail: str, status_code: int = 500):
    raise HTTPException(status_code=status_code, detail=detail)