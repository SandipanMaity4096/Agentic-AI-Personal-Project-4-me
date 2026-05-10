# Interview-Ready Explanation

## One-Line Pitch
I built an Agentic AI customer support chatbot that combines multi-agent orchestration, RAG-based knowledge retrieval, persistent memory, and automated escalation simulation for enterprise-style support workflows.

## How Agentic AI Works Internally
- Instead of using one prompt for everything, the system decomposes the task into specialized agents.
- Each agent solves a focused problem: intent extraction, sentiment scoring, retrieval, and escalation decisioning.
- The orchestrator composes outputs into one reliable final response.
- This pattern improves controllability, observability, and business-rule alignment.

## Why Not a Single LLM Call?
- Single calls are harder to debug and govern.
- Agent-based pipelines allow modular testing and policy injection.
- Better enterprise fit due to traceability and easier compliance checks.

## RAG and Memory
- RAG grounds answers in company policy documents stored in Chroma.
- Conversation state and ticket metadata are persisted in SQLite.
- This gives short-term contextual memory and operational logging.

## Human Escalation Design
- Negative sentiment or critical intents trigger escalation logic.
- System auto-creates a ticket and informs the user.
- This simulates a human-in-the-loop support center.

## Trade-offs and Design Choices
- Chose Streamlit for rapid enterprise demo velocity.
- Chose SQLite for low-ops persistence.
- Chose provider abstraction to stay vendor-neutral.

## What I Would Do in Production
- Add async task queue, role-based auth, and observability stack.
- Add policy engine, prompt versioning, and evaluation harness.
- Integrate real ticketing APIs such as Zendesk or Freshdesk.
