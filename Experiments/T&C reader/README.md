# T&C Reader

A quirky, user-friendly tool to read, summarize, and explain Terms & Conditions using AI.

## Features
- Upload or paste T&C text
- Summarizes T&C in simple language
- Three main focus areas:
  1. Data Usage & Privacy
  2. User Rights & Responsibilities
  3. Cancellation & Refunds
- Clickable, aesthetic UI with subcategories
- Summaries tailored by age group or tone (e.g., serious, comedy)

## Tech Stack
- **Backend:** Python (FastAPI), AI model (OpenAI or local LLM)
- **Frontend:** HTML, CSS, JavaScript

## Project Structure
```
T&C reader/
│
├── backend/
│   ├── main.py         # FastAPI app
│   ├── ai_utils.py     # AI model interaction
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── README.md
``` 