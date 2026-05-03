# Feature: Recruiter Agent System (v1.0)
Estado: [EN DESARROLLO] - Stress Test: [PENDIENTE DE VALIDACIÓN]

## 🎯 Propósito
Proporcionar una interfaz técnica y profesional para que reclutadores consulten el perfil de Juan Ortega con trazabilidad total del razonamiento de la IA.

## 🛠️ Stack Tecnológico
- **Backend**: FastAPI
- **Orquestación**: LangGraph (Ciclo: Input -> Retrieve -> Grade -> Generate)
- **Vector DB**: FAISS (Local)
- **Modelos**: OpenAI (GPT-4o para reasoning, Text-embedding-3-small)

## 🔄 Contrato de Datos (Input/Output)
### ChatRequest
- `message`: string (Pregunta del reclutador)

### ChatResponse
- `response`: string (Texto profesional)
- `steps`: list[string] (Nodos ejecutados en LangGraph)
- `context`: list[string] (Fragmentos de documentos usados)

## 🏗️ Lógica del Grafo (LangGraph)
1. **Node: retrieve**: Obtiene top-5 chunks de FAISS.
2. **Node: grade_docs**: (Stress Test Mitigation) Valida si los chunks responden a la pregunta.
3. **Node: transform_query**: Si los chunks no sirven, reformula para una segunda oportunidad.
4. **Node: generate**: Produce la respuesta final basada en el contexto validado.

## 🧪 Stress Test Cases (Aprobación Requerida)
- **Test 1 (Out of scope)**: "¿Cuál es el color favorito de Juan?". 
  - *Resultado esperado*: "No tengo información en el contexto profesional".
- **Test 2 (Ambiguous)**: "¿Sabe de Python?". 
  - *Resultado esperado*: Detallar proyectos específicos encontrados en el CV.
- **Test 3 (Conflicting data)**: Contradicción entre CV y Q&A. 
  - *Resultado esperado*: Priorizar el Q&A como fuente de "Verdad Actualizada".

---
> [!IMPORTANT]
> No se continuará con el desarrollo del Frontend hasta que el Backend supere estos tests conceptuales.
