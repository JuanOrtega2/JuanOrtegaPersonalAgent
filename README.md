# Personal AI Recruiter Agent

Senior AI Recruiter Agent built with LangGraph, Google Gemini, and RAG (Retrieval-Augmented Generation).

## Features
- LangGraph-based agentic workflow.
- RAG system for CV and Q&A processing.
- Professional executive recruiter tone.
- Built-in stress testing and guardrails.

## Setup

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Configure Environment**:
   Create a `.env` file in the root with:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Data**:
   Place your CV as `resume.pdf` and Q&A as `qa_knowledge.json` in the `data/` folder.

## Testing

Run tests with pytest:
```bash
uv run pytest
```

## Development

This project uses `pre-commit` to ensure code quality and run tests before every commit.
Hooks are installed automatically if you run:
```bash
uv run pre-commit install
```
