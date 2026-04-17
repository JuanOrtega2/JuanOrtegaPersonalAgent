import os
import sys

import pytest
from dotenv import load_dotenv

# Add project root to PATH
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_dir)

# Load environment variables
load_dotenv(os.path.join(root_dir, ".env"))

from backend.app.agent import RecruiterAgent
from backend.app.rag import RAGManager


@pytest.fixture
def agent(mocker):
    """Fixture with minimal mocking to ensure the test runs without external API calls."""
    mocker.patch("backend.app.rag.GoogleGenerativeAIEmbeddings")
    mocker.patch("backend.app.agent.ChatGoogleGenerativeAI")
    mocker.patch("backend.app.rag.PyPDFLoader")

    rag = RAGManager()
    # Mock vector store to avoid retrieve errors
    rag.vector_store = mocker.MagicMock()
    rag.vector_store.as_retriever.return_value.invoke.return_value = []

    return RecruiterAgent(rag)


@pytest.mark.asyncio
async def test_agent_structural_check(agent, mocker):
    """Verifies that the agent instance is correctly created and has the required methods."""
    assert agent is not None
    assert hasattr(agent, "run")
    assert agent.workflow is not None
