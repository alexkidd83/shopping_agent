# Shopping Agent

This repository contains the source code for a prototype **AI shopping agent**.  The
agent is designed to monitor a user’s Amazon orders, basket and saved items,
compare prices with the price comparison site **Idealo**, and automatically
generate product listings on **eBay** when a profitable opportunity exists.  It
implements the agentic framework outlined in the Product Compass diagram
(`How to Build an AI Agent?`), mapping each of the seven steps to concrete
components in this codebase.

## Repository Structure

```
shopping_agent/
├── README.md             — This file
├── main.py               — Entry point that wires up the agent
├── orchestrator.py       — Orchestration logic tying together tools and memory
├── memory.py             — Simple in‑memory and file‑based storage abstractions
├── eval.py               — Hooks for measuring and improving agent performance
├── ui.py                 — Command‑line interface to interact with the agent
├── prompts/
│   └── system_prompt.txt — Template for the agent’s system prompt
└── tools/
    ├── __init__.py       — Makes this a Python package
    ├── amazon_api.py     — Stub for communicating with Amazon (orders/basket)
    ├── idealo_api.py     — Stub for price comparison via Idealo
    ├── ebay_api.py       — Stub for creating listings on eBay
    └── email.py          — Stub for sending email reports/notifications
```

## How It Works

1. **System Prompt** — The base system prompt lives in `prompts/system_prompt.txt`.  It
   defines the agent’s role, goals and high‑level instructions.  When the
   agent is instantiated (see `main.py`), this prompt is used to prime the
   language model.
2. **LLM** — In this prototype we defer to a local stub for the language model.  It
   can be replaced with a call to an external API (e.g. OpenAI GPT) or a
   locally hosted model.  The `LLM` class encapsulates the interface.
3. **Tools** — The `tools` package contains modules that encapsulate external
   services.  Each module exposes high‑level functions for retrieving or
   sending data.  The stubs currently return mocked data for demonstration
   purposes.
4. **Memory** — The `memory` module provides a very simple episodic memory
   (list of past runs), a working memory for the current run and file‑based
   persistence.  A production agent would likely integrate with a vector
   database (e.g. FAISS, Pinecone) for similarity search.
5. **Orchestration** — The `orchestrator.py` module contains the logic to
   schedule and coordinate tasks: fetching Amazon data, comparing prices,
   deciding whether to list items on eBay and sending notifications.  It
   functions as the router/workflow engine described in the 7‑step process.
6. **UI** — A simple command‑line interface in `ui.py` triggers the agent’s
   workflow on demand.  This could be replaced with a web or mobile UI.
7. **AI Evals** — The `eval.py` module defines hooks to collect metrics (e.g.
   number of offers processed, conversion rate on eBay) and store them for
   later analysis.  Over time these metrics help refine the agent’s
   decision‑making.

## Running the Agent

1. Create a virtual environment and install dependencies (if any).  In this
   prototype there are no external dependencies aside from the Python
   standard library.

2. Run the CLI:

```bash
python3 -m shopping_agent.ui run
```

This will execute a single iteration of the agent’s workflow, printing
diagnostics to the console.  The code is structured to make it easy to plug
in real API calls and a persistent database when you are ready to move
beyond the prototype.

## Next Steps

To turn this into a fully functioning agent:

* Replace the stubbed API calls in `tools/` with actual integrations to
  Amazon, Idealo and eBay.  Each module should handle authentication,
  pagination and error handling.
* Integrate a language model in `main.py` by implementing the `call` method
  of the `LLM` class.  Consider using an external provider like OpenAI or
  deploying a local model for privacy.
* Swap out the in‑memory storage for a persistent database or vector store.
  This will allow the agent to remember past actions across runs.
* Build a richer UI with search/filter capabilities, perhaps using a web
  framework such as React or a low‑code platform.

This repository provides a skeleton that follows best practices for agentic
design, leaving room for expansion as you add real functionality.
