from settings import MAX_USER_INPUT
from fastapi import HTTPException

def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_USER_INPUT

def validate_api_length(prompt: str):
    if len(prompt) >= MAX_USER_INPUT:
        raise HTTPException(status_code=400, detail="Prompt length is too long.")