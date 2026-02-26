from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from backend.orchestrator import Orchestrator

# Load environment variables
load_dotenv()

app = FastAPI(title="Atlas Open Tutor API", description="Multi-Agent Backend for Avatar Room")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to Streamlit's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Orchestrator Singleton
api_key = os.getenv("MISTRAL_API_KEY", "")
api_key = api_key.strip().strip('"').strip("'")
orchestrator = Orchestrator(api_key=api_key)

class ChatRequest(BaseModel):
    avatar_id: str
    message: str
    mode: str = "chat"
    material: str = ""

class ResetRequest(BaseModel):
    avatar_id: str

@app.post("/api/chat")
async def chat_with_agent(req: ChatRequest):
    """Route a message to the specific agent and get its response."""
    if not api_key:
        raise HTTPException(status_code=500, detail="Mistral API key not configured on backend.")
        
    try:
        response = orchestrator.process_request(
            avatar_id=req.avatar_id,
            message=req.message,
            mode=req.mode,
            material=req.material
        )
        return {"reply": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reset")
async def reset_agent_memory(req: ResetRequest):
    """Clear an agent's conversation history."""
    orchestrator.reset_agent(req.avatar_id)
    return {"status": "success"}

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "agents_loaded": len(orchestrator.agents)}
