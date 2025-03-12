# src/app/core/config.py
import torch

class Settings:
    model_name: str = "facebook/seamless-m4t-v2-large"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

settings = Settings()