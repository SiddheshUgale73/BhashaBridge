import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI-compatible client pointing to Groq
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# ─── Supported Languages ────────────────────────────────────────────────────
SUPPORTED_LANGUAGES = {
    "Hindi", "Marathi", "English", "Gujarati", "Tamil",
    "Telugu", "Kannada", "Bengali", "Punjabi", "Urdu"
}

# ─── System Prompt ──────────────────────────────────────────────────────────
def _build_system_prompt(target_language: str) -> str:
    return f"""You are BhashaBridge, an expert AI language assistant and professional translator specializing in Indian and world languages.

Your job is to:
1. Understand the TRUE MEANING and INTENT of the user's input — even if it has grammatical mistakes, is informal, uses slang, or is in mixed language (e.g., Hinglish).
2. Produce a grammatically corrected version of the input in its ORIGINAL language.
3. Translate it naturally and fluently into {target_language}, exactly as a native {target_language} speaker would say it.

CRITICAL RULES:
- DO NOT translate word-by-word. Capture the meaning and produce a natural, idiomatic sentence.
- If the input is already grammatically correct, the corrected_text should be the same as the input.
- If the input is already in {target_language}, still return the corrected version and the translation (translation can be the same text).
- Preserve tone: if input is formal, keep it formal. If casual/friendly, keep it casual.
- For Indian languages (Hindi, Marathi, Gujarati, etc.), use the native script (Devanagari, etc.) for the translated_text.
- NEVER include explanations, notes, or extra text outside the JSON.
- ALWAYS respond ONLY with a valid JSON object in this exact format:

{{
  "corrected_text": "<grammatically corrected input in original language>",
  "translated_text": "<natural, fluent translation in {target_language}>"
}}

Examples:
Input: "i am go to market yesterday"
Output: {{"corrected_text": "I went to the market yesterday.", "translated_text": "मैं कल बाजार गया था।"}} (if target is Hindi)

Input: "muje bhook lagi hai"
Output: {{"corrected_text": "मुझे भूख लगी है।", "translated_text": "I am hungry."}} (if target is English)
"""

# ─── Core Translation Function ───────────────────────────────────────────────
def translate_text(text: str, target_language: str) -> dict:
    """
    Translates input text to the target language with grammar correction.

    Args:
        text (str): The input text to be translated.
        target_language (str): The target language name (e.g., "Hindi", "Marathi").

    Returns:
        dict: A dictionary with 'corrected_text' and 'translated_text'.
    """
    # ── Input validation ──
    text = text.strip()
    if not text:
        return {"corrected_text": "", "translated_text": "", "error": "Input text is empty."}

    if len(text) > 2000:
        return {"corrected_text": "", "translated_text": "", "error": "Input is too long. Maximum 2000 characters."}

    if target_language not in SUPPORTED_LANGUAGES:
        print(f"[WARN] Unsupported language requested: {target_language}")

    system_prompt = _build_system_prompt(target_language)

    # ── API call with retry ──
    last_error = None
    for attempt in range(2):  # Retry once on failure
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Upgraded: much more accurate for translation
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate this to {target_language}:\n\n{text}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
                max_tokens=1024,
                top_p=0.9,
            )

            raw = response.choices[0].message.content.strip()

            # Strip markdown fences if model ignores instructions
            raw = re.sub(r"^```(?:json)?", "", raw).strip()
            raw = re.sub(r"```$", "", raw).strip()

            result = json.loads(raw)

            corrected = result.get("corrected_text", "").strip()
            translated = result.get("translated_text", "").strip()

            if not translated:
                raise ValueError("Model returned empty translated_text.")

            return {
                "corrected_text": corrected or text,
                "translated_text": translated,
            }

        except (json.JSONDecodeError, ValueError) as e:
            last_error = f"Parsing error on attempt {attempt + 1}: {str(e)}"
            print(f"[ERROR] {last_error}")
        except Exception as e:
            last_error = str(e)
            print(f"[ERROR] API error on attempt {attempt + 1}: {last_error}")
            break

    return {
        "error": last_error or "Translation failed after retries.",
        "corrected_text": "",
        "translated_text": ""
    }
