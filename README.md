# Agentic AI Customer Support Chatbot

A practical, enterprise-demo style project showing Agentic AI + RAG + memory + escalation automation without heavy backend frameworks.

## Tech Stack

- Python 3.10+
- Streamlit (UI)
- LangChain (agent workflow utilities)
- OpenAI / Gemini / Ollama (LLM options)
- ChromaDB (vector database for RAG)
- SQLite (conversation and ticket storage)

## Business Problem Solved

Customer support teams need fast, consistent, and context-aware responses while still escalating critical cases to humans. This project simulates that workflow with multiple collaborating AI agents.

## Key Features

1. AI-powered support chat assistant
2. Multi-agent orchestration
3. Specialized agents:
- Customer Query Agent
- FAQ Retrieval Agent
- Sentiment Analysis Agent
- Escalation Agent
4. Context-aware history via SQLite logs
5. File-based KB ingestion (TXT/PDF)
6. RAG-grounded responses from vector DB
7. Auto-ticket creation simulation
8. Human escalation simulation
9. Dashboard for conversations and tickets

## Architecture

See docs/architecture.md for detailed architecture and Mermaid diagram.

### Internal Flow

1. User sends query in Streamlit UI.
2. Orchestrator dispatches query to Customer Query Agent and Sentiment Agent.
3. FAQ Retrieval Agent performs semantic search from Chroma vector DB.
4. Escalation Agent evaluates risk and customer dissatisfaction.
5. Orchestrator composes final response.
6. Conversation and trace are stored in SQLite.
7. If escalated, ticket is auto-created and displayed in dashboard.

## Project Structure

```
Agentic AI Personal Project/
  app/
    main.py
  agents/
    base_agent.py
    customer_query_agent.py
    faq_retrieval_agent.py
    sentiment_analysis_agent.py
    escalation_agent.py
  core/
    config.py
    llm.py
    vector_store.py
    db.py
    orchestrator.py
  data/
    knowledge_base/
      faq.txt
  docs/
    architecture.md
    demo-scenarios.md
    interview-guide.md
    resume-project-description.md
  prompts/
    system_support_prompt.txt
  scripts/
    ingest_kb.py
  tests/
    test_orchestrator.py
  storage/
  .env.example
  .gitignore
  requirements.txt
  README.md
```

## Setup Instructions

1. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Configure environment variables

```powershell
Copy-Item .env.example .env
```

Update .env with one provider:
- OpenAI: OPENAI_API_KEY
- Gemini: GOOGLE_API_KEY
- Ollama: ensure local Ollama service is running

4. Ingest knowledge base into vector store

```powershell
python scripts/ingest_kb.py
```

5. Run the app

```powershell
streamlit run app/main.py
```

## End-to-End Implementation Plan

### Phase 1: Foundation
- Set up folder structure and configs
- Add provider-agnostic LLM layer
- Add SQLite schemas for conversations and tickets

### Phase 2: Intelligence Layer
- Build Customer Query Agent for intent/urgency
- Build Sentiment Analysis Agent
- Build FAQ Retrieval Agent with Chroma RAG
- Build Escalation Agent with policy rules

### Phase 3: Orchestration
- Build AgentOrchestrator pipeline
- Add traceability and data logging
- Add escalation ticket creation simulation

### Phase 4: Experience and Demo
- Build Streamlit chat + dashboard UI
- Add realistic FAQ knowledge files
- Prepare scenarios and interview notes

## Sample Prompts

- "I cannot login after changing my phone."
- "You charged me twice and I need a refund today."
- "This is unacceptable, I want to speak to your manager now."
- "Where is my shipment? It has been 12 days."

## Real-World Use Cases

- E-commerce support for delivery and return disputes
- SaaS support for login, billing, and outage incidents
- Fintech support triage with sentiment-aware escalation
- Telecom support with policy-grounded first responses

## How to Present This to a Project Manager

- Position it as a "Support Operations Co-Pilot".
- Show modular agents as independent services.
- Highlight faster first response time and reduced manual triage.
- Emphasize audit trail and escalations for compliance and trust.

## Future Enhancements

1. Replace rule-based escalation with learned policy model.
2. Add Redis for short-term memory cache.
3. Integrate Zendesk/Freshdesk/Jira APIs for real ticket creation.
4. Add authentication and role-based dashboards.
5. Add observability stack (OpenTelemetry + LangSmith traces).
6. Add multilingual support and voice channel.
7. Add evaluation harness for answer quality and hallucination checks.

## Interview Q and A Prep

Q: What makes this "Agentic AI"?
A: The system decomposes support handling into specialized agents coordinated by an orchestrator, instead of relying on a single monolithic LLM call.

Q: Where is RAG used?
A: FAQ Retrieval Agent embeds KB files in Chroma and retrieves relevant chunks at runtime to ground responses.

Q: How does memory work?
A: SQLite stores session history, intent/sentiment metadata, and tickets, enabling context retention and operational analytics.

Q: How do you control hallucination risk?
A: Responses are grounded by retrieval context, constrained prompts, and escalation fallback for sensitive cases.

## Notes

- This is a demo-oriented architecture that is beginner-friendly but production-minded.
- If no provider key is set, fallback mode still demonstrates workflow and UI.
