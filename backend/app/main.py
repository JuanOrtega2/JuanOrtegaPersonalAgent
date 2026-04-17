from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .rag import RAGManager
from .agent import RecruiterAgent
from .schemas import ChatRequest, ChatResponse
import os

app = FastAPI(title="Recruiter AI Agent API")

# Setup CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables para mantener el estado (en prod usarías una DB o Cache)
rag_manager = RAGManager()
agent = None

@app.on_event("startup")
async def startup_event():
    global agent
    print("Iniciando sistema RAG...")
    
    # Ingestión inicial del CV
    cv_path = "c:/Users/juano/Documents/repos/personal/JuanOrtegaPersonalAgent/data/CV_JuanOrtega_English_updated.pdf"
    qa_path = "c:/Users/juano/Documents/repos/personal/JuanOrtegaPersonalAgent/data/qa_knowledge.json"
    
    if os.path.exists(cv_path):
        count = rag_manager.ingest_cv(cv_path)
        print(f"CV procesado: {count} documentos.")
    
    if os.path.exists(qa_path):
        count = rag_manager.ingest_qa(qa_path)
        print(f"Q&A procesado: {count} documentos.")
    
    # Inicializar Agente
    agent = RecruiterAgent(rag_manager)
    print("Agente de reclutamiento listo.")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if agent is None:
        raise HTTPException(status_code=503, detail="Agente no inicializado")
    
    try:
        result = await agent.run(request.message)
        return ChatResponse(
            response=result["response"],
            steps=result["steps"],
            context=result["context"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "agent_ready": agent is not None}
