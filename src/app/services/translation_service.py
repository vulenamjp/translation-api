# src/app/services/translation_service.py
import torch
from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText
from app.core.config import settings  # Import settings
from typing import List

class SeamlessTranslator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SeamlessTranslator, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if not self.initialized:
            print("Initializing translator...")
            self.processor = AutoProcessor.from_pretrained(settings.model_name)
            self.model = SeamlessM4Tv2ForTextToText.from_pretrained(settings.model_name)
            self.device = settings.device
            self.model.to(self.device)
            print(f"Model loaded on {self.device}")
            self.initialized = True

    def translate_text(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Dịch một chuỗi văn bản"""
        text_inputs = self.processor(
            text=text,
            src_lang=src_lang,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            output_tokens = self.model.generate(
                input_ids=text_inputs.input_ids,
                attention_mask=text_inputs.attention_mask,
                tgt_lang=tgt_lang,
                max_length=1024
            )

        translated_text = self.processor.decode(output_tokens[0], skip_special_tokens=True)
        return translated_text

    def translate_batch(self, texts: List[str], src_lang: str, tgt_lang: str) -> List[str]:
        """Dịch một mảng các chuỗi văn bản"""
        results = []
        for text in texts:
            translated = self.translate_text(text, src_lang, tgt_lang)
            results.append(translated)
        return results

translator_service = SeamlessTranslator() # Instance singleton service