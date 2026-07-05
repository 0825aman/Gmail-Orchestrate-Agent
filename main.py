"""
main.py
-------
FastAPI server for the Gmail Agentic AI.

Endpoints:
  GET  /        → Chat UI  (HTML — rendered from ui.py)
  GET  /health  → JSON health check
  POST /chat    → Natural language Gmail assistant (JSON API — unchanged)
  GET  /docs    → Swagger UI

Run:
  python -m uvicorn main:app --reload

Local URLs:
  http://127.0.0.1:8000        (Chat UI)
  http://127.0.0.1:8000/docs   (Swagger UI)
  http://127.0.0.1:8000/health (Health check JSON)
"""
import setup_files #Added for deployment on Render

import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from agent import run_agent
from ui import HTML_PAGE          # ← upgraded UI lives in ui.py

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Gmail Agentic AI",
    description=(
        "A natural language Gmail assistant powered by IBM WatsonX "
        "(granite-4-h-small) and LangGraph. "
        "Send plain-English commands to list, read, write, or delete emails."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str

    class Config:
        json_schema_extra = {
            "example": {"message": "List my last 5 emails"}
        }


class ChatResponse(BaseModel):
    reply: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Serves the Gmail Agent chat UI (see ui.py for the HTML source)."""
    return HTMLResponse(content=HTML_PAGE)


@app.get("/health", summary="Health Check")
async def health():
    """Returns JSON status."""
    return {"status": "Gmail Agent is running", "docs": "http://127.0.0.1:8000/docs"}


@app.post("/chat", response_model=ChatResponse, summary="Chat with the Gmail Agent")
async def chat(request: ChatRequest):
    """
    Send a natural language message to the Gmail agent.

    **Examples:**
    - `"List my last 5 emails"`
    - `"Read the email with ID 18f3a2b1c4d5e6f7"`
    - `"Send an email to alice@example.com with subject Hello and body Hi there!"`
    - `"Permanently delete the email with ID 18f3a2b1c4d5e6f7"`
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        reply = await asyncio.to_thread(run_agent, request.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(exc)}")

    return ChatResponse(reply=reply)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
