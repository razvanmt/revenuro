from fastapi import FastAPI
from functions import validate_api_length
from application import generate_branding_snippet, generate_keywords
from settings import MAX_USER_INPUT
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)


@app.get("/generate-snippets")
async def r_generate_snippet(prompt: str):
    validate_api_length(prompt)
    snippet = generate_branding_snippet(prompt)
    return {"snippet": snippet, "keywords": None}


@app.get("/generate-keywords")
async def r_generate_keyword(prompt: str):
    validate_api_length(prompt)
    keywords = generate_keywords(prompt)
    return {"snippet": None, "keywords": keywords}


@app.get("/generate-branding")
async def r_generate_branding(prompt: str):
    validate_api_length(prompt)
    snippet = generate_branding_snippet(prompt)
    keywords = generate_keywords(prompt)
    return {"snippet": snippet, "keywords": keywords}
