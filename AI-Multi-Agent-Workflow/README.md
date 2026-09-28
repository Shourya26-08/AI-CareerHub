# AI Multi-Agent Workflow

A modular Python + LLM multi-agent workflow that decomposes complex tasks, assigns specialist agents, passes shared context, reviews outputs, and synthesizes a final response.

## Architecture
User Task -> Planner -> Specialist Agents -> Critic -> Synthesizer -> Final Response

## Features
- Task decomposition and structured plans
- Role-based Researcher, Analyst, Writer, and Engineer agents
- Shared workflow context
- Parallel specialist execution
- Critic/review pass
- Structured Pydantic outputs
- Tool registry with calculator
- Modular extension points for RAG, APIs, databases and enterprise integrations

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API key.

```bash
python main.py "Create a 30-day plan to learn backend development"
```

## Project Structure
- `main.py` - CLI entry point
- `workflow.py` - orchestration engine
- `llm.py` - LLM client
- `schemas.py` - structured workflow models
- `agents/` - planner, specialists, critic and synthesizer
- `tools/` - reusable tool registry and calculator
