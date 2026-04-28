from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from translator import translate_text

# Initialize FastAPI App
app = FastAPI(
    title="BhashaBridge API",
    description="AI-powered language translation system",
    version="1.0.0"
)

# Add CORS Middleware so frontends can communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the expected Input data structure using Pydantic
class TranslationRequest(BaseModel):
    text: str
    target_language: str

# Define the expected Output data structure using Pydantic
class TranslationResponse(BaseModel):
    corrected_text: str
    translated_text: str

# Create the POST /translate endpoint
@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translates the provided text into the target language, while correcting grammar.
    """
    try:
        # Call the translate_text function from translator.py
        result = translate_text(request.text, request.target_language)
        
        # Check if our translation function returned an error internally
        if "error" in result and result["error"]:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return TranslationResponse(
            corrected_text=result.get("corrected_text", ""),
            translated_text=result.get("translated_text", "")
        )
        
    except Exception as e:
        # Catch any unexpected errors and return a clean HTTP error
        raise HTTPException(status_code=500, detail=str(e))

# To run the server for testing:
# uvicorn main:app --reload
