from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .ai_utils import summarize_tc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummaryRequest(BaseModel):
    tc_text: str
    category: str  # 'data', 'rights', 'cancellation'
    tone: Optional[str] = 'serious'
    age_group: Optional[str] = 'adult'

@app.post("/summarize/")
def summarize(request: SummaryRequest):
    summary = summarize_tc(request.tc_text, request.category, request.tone, request.age_group)
    return {"summary": summary} 