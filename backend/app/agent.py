import os
from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from .rag import RAGManager
from .schemas import AgentState


class GradeDocuments(BaseModel):
    """Relevance rating for retrieved documents."""

    binary_score: str = Field(
        description="Are the documents relevant to the question? 'yes' or 'no'"
    )


class RecruiterAgent:
    def __init__(self, rag_manager: RAGManager):
        self.rag_manager = rag_manager
        # Use Gemini Flash for speed and cost-efficiency
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        self.workflow = self._create_graph()

    def _create_graph(self):
        workflow = StateGraph(AgentState)

        # Define Nodes
        workflow.add_node("retrieve", self.retrieve_node)
        workflow.add_node("grade_documents", self.grade_documents_node)
        workflow.add_node("generate", self.generate_node)
        workflow.add_node("transform_query", self.transform_query_node)

        # Define Flow and Conditionals
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "grade_documents")

        workflow.add_conditional_edges(
            "grade_documents",
            self.decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )

        workflow.add_edge("transform_query", "retrieve")
        workflow.add_edge("generate", END)

        return workflow.compile()

    def retrieve_node(self, state: AgentState):
        """Retrieves documents from the Vector DB."""
        retriever = self.rag_manager.get_retriever()
        docs = retriever.invoke(state.query)
        context = [d.page_content for d in docs]
        return {
            "context": context,
            "steps": state.steps + ["Retrieved context from Gemini Knowledge Base"],
        }

    def grade_documents_node(self, state: AgentState):
        """Evaluates whether retrieved documents are useful."""
        structured_llm = self.llm.with_structured_output(GradeDocuments)

        prompt = ChatPromptTemplate.from_template("""
        You are a grader evaluating relevance of retrieved documents to a user question.
        If the documents contain keywords or semantic meaning related to the user question, grade them as relevant.
        Give a binary score 'yes' or 'no' to indicate whether the documents are relevant to the question.
        
        Question: {query}
        Documents: {context}
        """)

        chain = prompt | structured_llm
        result = chain.invoke({"query": state.query, "context": "\n".join(state.context)})

        is_relevant = result.binary_score == "yes"
        return {
            "relevant": is_relevant,
            "steps": state.steps
            + [f"Gemini Relevance check: {'Passed' if is_relevant else 'Failed'}"],
        }

    def transform_query_node(self, state: AgentState):
        """Reformulates the question if initial retrieval was unsuccessful (one attempt only)."""
        if "Query reformulated" in state.steps:
            return {"steps": state.steps + ["Second attempt failed, moving to final generator"]}

        prompt = ChatPromptTemplate.from_template("""
        The previous retrieval did not return relevant information for the question: "{query}"
        Rewrite the question to improve retrieval, focusing on technical professional aspects related to Juan Ortega's profile.
        Only output the new question.
        """)

        chain = prompt | self.llm
        new_query = chain.invoke({"query": state.query})

        return {
            "query": new_query.content,
            "steps": state.steps + ["Query reformulated by Gemini"],
        }

    def generate_node(self, state: AgentState):
        """Generates the final response."""
        if not state.relevant and "Query reformulated" in state.steps:
            return {
                "response": "Based on the candidate's core profile and the provided professional Q&A, I don't have enough specific information to answer that accurately. Is there anything else about Juan's technical background I can help you with?",
                "steps": state.steps + ["Admitted lack of specific information"],
            }

        prompt = ChatPromptTemplate.from_template("""
        You are Juan Ortega's Professional AI Agent (Executive Recruiter Tone).
        Use the following context to answer the question about the candidate.
        
        Context: {context}
        Question: {query}
        
        Guidelines:
        - If the info is NOT in context, politely say you don't have that specific data.
        - Be concise and professional.
        - Use Markdown.
        """)

        chain = prompt | self.llm
        response = chain.invoke({"context": "\n".join(state.context), "query": state.query})

        return {
            "response": response.content,
            "steps": state.steps + ["Generated final response via Gemini"],
        }

    def decide_to_generate(self, state: AgentState) -> Literal["transform_query", "generate"]:
        """Decides whether to try search again or generate the response."""
        if state.relevant or "Query reformulated" in state.steps:
            return "generate"
        else:
            return "transform_query"

    async def run(self, query: str):
        """Runs the agent workflow for a given query."""
        inputs = {"query": query, "steps": [], "relevant": True}
        result = await self.workflow.ainvoke(inputs)
        return result
