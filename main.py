from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from translator import translate_text
import os

# Initialize FastAPI App
app = FastAPI(
    title="BhashaBridge API",
    description="AI-powered language translation system",
    version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Serve the Chat UI at the root ───────────────────────────────────────────
# This makes visiting http://127.0.0.1:8000 open the Chat UI directly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_HTML = os.path.join(BASE_DIR, "index.html")

@app.get("/", response_class=FileResponse)
async def serve_ui():
    """Serves the BhashaBridge Chat UI."""
    return FileResponse(FRONTEND_HTML)

# ─── API Models ───────────────────────────────────────────────────────────────
class TranslationRequest(BaseModel):
    text: str
    target_language: str

class TranslationResponse(BaseModel):
    corrected_text: str
    translated_text: str

# ─── Translation Endpoint ─────────────────────────────────────────────────────
@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translates the provided text into the target language, while correcting grammar.
    """
    try:
        result = translate_text(request.text, request.target_language)

        if "error" in result and result["error"]:
            raise HTTPException(status_code=500, detail=result["error"])

        return TranslationResponse(
            corrected_text=result.get("corrected_text", ""),
            translated_text=result.get("translated_text", "")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── Run Instructions ─────────────────────────────────────────────────────────
# Step 1: uvicorn main:app --reload
# Step 2: Open http://127.0.0.1:8000 in your browser
