import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client for xAI (Grok)
# Assumes GROK_API_KEY is set in the environment or .env file
client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1",
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
Do NOT translate word-by-word. Focus on the natural expression and informal or incorrect English handling.

You MUST respond ONLY with a JSON object in the following format:
{{
    "corrected_text": "The grammatically corrected version of the original input",
    "translated_text": "The natural and fluent translation in {target_language}"
}}
"""

    try:
        response = client.chat.completions.create(
            model="grok-beta", # Using xAI's grok model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            response_format={ "type": "json_object" },
            temperature=0.3, # Lower temperature for more deterministic/translation tasks
        )
        
        # Parse the JSON response from OpenAI
        result_json = response.choices[0].message.content
        return json.loads(result_json)
        
    except Exception as e:
        # In a real system, you might want to log this or raise a custom exception
        return {
            "error": str(e),
            "corrected_text": "",
            "translated_text": ""
        }

if __name__ == "__main__":
    # Example usage
    sample_text = "I likes to her"
    target_lang = "Hindi"
    
    print(f"Input: '{sample_text}' | Target Language: {target_lang}")
    result = translate_text(sample_text, target_lang)
    print(json.dumps(result, indent=2, ensure_ascii=False))
