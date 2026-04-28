# BhashaBridge

BhashaBridge is an AI-powered language translation system that goes beyond simple word-by-word translation. It intelligently understands the meaning of the input text, corrects any grammatical errors in the original language, and provides a natural, fluent translation in the target language.

## Features

- **Grammar Correction**: Automatically detects and fixes grammatical mistakes in the input text before translating.
- **Natural Translation**: Uses advanced AI (Groq + Llama 3.1) to ensure the translation sounds natural to native speakers, avoiding awkward literal translations.
- **Minimalist UI**: A clean, modern, and easy-to-use web interface.
- **FastAPI Backend**: A highly performant and scalable Python backend.

## Tech Stack

- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (Vanilla)
- **Backend**: Python 3, FastAPI, Uvicorn, Pydantic
- **AI Integration**: Groq API (Llama-3.1-8b-instant), OpenAI Python SDK
- **Environment**: python-dotenv

## Project Structure

```
BhashaBridge/
│
├── frontend/
│   └── index.html         # The minimalist UI
│
└── backend/
    ├── main.py            # FastAPI server and endpoints
    ├── translator.py      # Core AI translation logic
    ├── requirements.txt   # Python dependencies
    ├── .env.example       # Example environment variables
    └── .env               # Your actual environment variables (Git ignored)
```

## Setup Steps

### 1. Backend Setup

Open your terminal and navigate to the `backend` folder:
```bash
cd backend
```

Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

Set up your API Key:
1. Rename `.env.example` to `.env` (or just create a `.env` file).
2. Add your Groq API key:
   ```env
   GROQ_API_KEY=your_actual_key_here
   ```

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The backend will now be running on `http://127.0.0.1:8000`.

### 2. Frontend Setup

You do not need any special servers to run the frontend. Simply open the `frontend/index.html` file in any modern web browser (Chrome, Edge, Firefox, etc.).

1. Navigate to the `frontend/` folder.
2. Double-click `index.html`.
3. Type your text, select a language, and click "Translate"!
