# src/app/api/endpoints/translation.py
from fastapi import APIRouter, BackgroundTasks, Depends
from app.schemas.translation import TranslationRequest, TranslationResponse, BatchTranslationRequest, BatchTranslationResponse
from app.services.translation_service import SeamlessTranslator
from app.api.dependencies import get_translator_service
from app.api.exceptions import translation_exception_handler

router = APIRouter()

@router.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest, translator_service: SeamlessTranslator = Depends(get_translator_service)):
    try:
        translated_text = translator_service.translate_text(
            request.text, request.source_lang, request.target_lang
        )
        return {"translated_text": translated_text}
    except Exception as e:
        translation_exception_handler(detail=f"Lỗi dịch: {str(e)}")

@router.post("/translate-batch", response_model=BatchTranslationResponse)
async def translate_batch(request: BatchTranslationRequest, background_tasks: BackgroundTasks, translator_service: SeamlessTranslator = Depends(get_translator_service)):
    try:
        if len(request.texts) > 20:
            translated_texts = []
            translated_texts = translator_service.translate_batch(
                request.texts[:5], request.source_lang, request.target_lang
            )
            background_tasks.add_task(
                translator_service.translate_batch,
                request.texts[5:],
                request.source_lang,
                request.target_lang
            )
            return {"translated_texts": translated_texts}
        else:
            translated_texts = translator_service.translate_batch(
                request.texts, request.source_lang, request.target_lang
            )
            return {"translated_texts": translated_texts}
    except Exception as e:
        translation_exception_handler(detail=f"Lỗi dịch batch: {str(e)}")

@router.get("/languages")
async def get_supported_languages():
    languages = {
        "eng": "English",
        "vie": "Vietnamese",
        "fra": "French",
        "deu": "German",
        "spa": "Spanish",
        "ita": "Italian",
        "por": "Portuguese",
        "rus": "Russian",
        "cmn": "Chinese (Mandarin)",
        "jpn": "Japanese",
        "kor": "Korean",
        "ara": "Arabic",
        "hin": "Hindi",
        "ben": "Bengali",
        "tha": "Thai",
        "ind": "Indonesian"
    }
    return languages