import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .agent import RecruiterAgent
from .rag import RAGManager
from .schemas import ChatRequest, ChatResponse

app = FastAPI(title="Recruiter AI Agent API")

# Setup CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to maintain state (in production consider DB or Cache)
rag_manager = RAGManager()
agent = None


@app.on_event("startup")
async def startup_event():
    global agent
    print("Starting RAG system...")

    # Initial ingestion of the resume
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cv_path = os.path.join(base_dir, "data", "resume.pdf")
    qa_path = os.path.join(base_dir, "data", "qa_knowledge.json")

    if os.path.exists(cv_path):
        count = rag_manager.ingest_cv(cv_path)
        print(f"Resume processed: {count} documents.")

    if os.path.exists(qa_path):
        count = rag_manager.ingest_qa(qa_path)
        print(f"Q&A processed: {count} documents.")

    # Initialize the Agent
    agent = RecruiterAgent(rag_manager)
    print("Recruiter Agent ready.")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:
        result = await agent.run(request.message)
        return ChatResponse(
            response=result["response"],
            steps=result["steps"],
            context=result["context"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok", "agent_ready": agent is not None}
