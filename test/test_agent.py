import asyncio
import os
import sys
from dotenv import load_dotenv

# Añadir la raíz del proyecto al PATH de forma automática
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)

# Cargar .env desde la raíz explícitamente
load_dotenv(os.path.join(root_dir, ".env"))

from backend.app.rag import RAGManager
from backend.app.agent import RecruiterAgent

async def test():
    print("🚀 Iniciando Stress Test del Agente (Google Gemini Edition)...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ ERROR: No se encuentra GOOGLE_API_KEY en el archivo .env")
        return

    # 1. Preparar RAG
    rag = RAGManager()
    cv_path = os.path.join(root_dir, 'CV_JuanOrtega_English_updated.pdf')
    
    if not os.path.exists(cv_path):
        print(f"❌ ERROR: No se encuentra el CV en {cv_path}")
        return

    print("📄 Ingestando CV...")
    rag.ingest_cv(cv_path)
    
    # Ingestar Q&A si existe
    qa_path = os.path.join(root_dir, 'data/qa_knowledge.json')
    if os.path.exists(qa_path):
        print("📂 Ingestando Q&A adicional...")
        rag.ingest_qa(qa_path)

    # 2. Iniciar Agente
    agent = RecruiterAgent(rag)
    
    # Test 1: Pregunta Técnica Real
    print("\n--- TEST 1: Información Profesional ---")
    print("Pregunta: 'What is Juan's experience with AI Agent architectures?'")
    res1 = await agent.run("What is Juan's experience with AI Agent architectures?")
    print(f"PASOS: {res1.get('steps', [])}")
    print(f"RESPUESTA:\n{res1.get('response', 'Sin respuesta')}")
    
    # Test 2: Pregunta Irrelevante (Stress Test)
    print("\n--- TEST 2: Pregunta Irrelevante ---")
    print("Pregunta: 'Does Juan like skiing?'")
    res2 = await agent.run("Does Juan like skiing?")
    print(f"PASOS: {res2.get('steps', [])}")
    print(f"RESPUESTA:\n{res2.get('response', 'Sin respuesta')}")

if __name__ == "__main__":
    asyncio.run(test())
