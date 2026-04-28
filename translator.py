import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client for Groq
# Assumes GROQ_API_KEY is set in the environment or .env file
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def translate_text(text: str, target_language: str) -> dict:
    """
    Translates text to the target language while correcting grammar and ensuring natural phrasing.
    
    Args:
        text (str): The input text to be translated.
        target_language (str): The language to translate the text into.
        
    Returns:
        dict: A dictionary containing 'corrected_text' and 'translated_text'.
    """
    system_prompt = f"""You are BhashaBridge, an AI-powered language translation system. 
Your task is to understand the meaning of the user's sentence, correct any grammatical errors in the original language, and then translate it naturally and fluently into {target_language}.

RULES:
1. `corrected_text` MUST be grammatically correct and preserve the original meaning.
2. `translated_text` MUST be natural and meaningful (do NOT translate word-by-word).
3. You MUST respond ONLY with valid JSON. Do not include any extra text, explanations, or markdown blocks outside the JSON object.

Return format:
{{
  "corrected_text": "...",
  "translated_text": "..."
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Using Groq's current Llama 3.1 model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            response_format={ "type": "json_object" },
            temperature=0.3, # Lower temperature for more deterministic/translation tasks
        )
        
        # Parse the JSON response from OpenAI
        result_text = response.choices[0].message.content
        
        # Clean up any potential markdown code blocks returned by the model
        result_text = result_text.strip()
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        elif result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
            
        return json.loads(result_text.strip())
        
    except Exception as e:
        # In a real system, you might want to log this or raise a custom exception
        return {
            "error": str(e),
            "corrected_text": "",
            "translated_text": ""
        }

