# Multi-Agent AI Travel Orchestrator via LangGraph

An advanced Multi-Agent Artificial Intelligence system built on top of LangGraph and LangChain. The project implements an enterprise-grade modular orchestration architecture where a central Orchestrator manages specialized agents to construct complete, structured travel itineraries based on single-string human constraints.

## Project Purpose and Core Capabilities

The primary goal of this system is to eliminate the need for manual context parsing and sequential step execution when planning travel. Instead of traditional monolithic chatbot loops, this system utilizes a directed acyclic graph (DAG) workflow with programmatic safety boundaries to deliver high-density, accurate, and financially verified results.

### What the System Does
1. **Dynamic Task Allocation:** The system accepts an unformatted natural language request containing location, duration, and financial boundaries.
2. **Context Preservation:** Utilizing a centralized custom state object (`OrchestratorState`), information passes transparently between dedicated domains without structural or context degradation.
3. **Deterministic Financial Verification:** Instead of allowing the Large Language Model (LLM) to perform mental math, the system routes financial checks directly to an isolated Python REPL runtime interpreter to ensure absolute mathematical precision.

---

## Architectural Layout and System Structure

The repository utilizes a modular approach designed for testability, scalability, and loose coupling of business logic.

```text
ai-travel-orchestrator-mvp/
│
├── agents/                  # Logic loops, core prompts, and LLM boundaries
│   ├── __init__.py          # Python package initializer
│   ├── orchestrator.py      # Central routing agent (The decision maker)
│   ├── planner.py           # Logistics specialist (Processes flight & hotel data)
│   ├── guide.py             # Cultural expert (Constructs day-by-day sightseeing)
│   └── budget.py            # Financial controller (Validates expenses vs limit)
│
├── tools/                   # External APIs and programmatic execution runtimes
│   ├── __init__.py          # Python package initializer
│   ├── google_serp.py       # High-performance API tools for flight and hotel scraping
│   ├── cultural_search.py   # Wikipedia query runs and live web scraping engines
│   └── calculator.py        # Isolated Python REPL sandbox for budget summation
│
├── graph/                   # Workflow lifecycle construction and compilation
│   ├── __init__.py          # Python package initializer
│   ├── state.py             # Global OrchestratorState with custom list/dict Reducers
│   ├── models.py            # Centralized, non-cyclic LLM model initialization
│   ├── workflow.py          # StateGraph instantiation and conditional edge pairing
│   └── router.py            # Strictly typed conditional edge mapping logic
│
├── .env.example             # Clean template configuration for required API keys
├── .gitignore               # Isolation rules for caching, venv, and sensitive .env data
├── app.py                   # System entry point and real-time execution loop
└── requirements.txt         # Pinned execution dependencies
```

---

## Execution Flow and Deep Dive

The process lifecycle operates strictly under the supervision of the Central Orchestrator node:

```text
[User Request] 
      │
      ▼
[Orchestrator] ──(Checks State Flags)
      │
      ├──► [Travel Planner] ──► (Calls Google Flights & Hotels Tools) ──► (Saves Lists to State)
      │
      ├──► [Guide]          ──► (Calls Wikipedia & Live Search Tools)  ──► (Saves Day Itinerary)
      │
      └──► [Budget Expert]  ──► (Calls Python REPL Math Engine)        ──► (Validates Limits)
      │
      ▼
   [END] (Outputs Compiled Document)
```

1. **State Evaluation:** The Orchestrator analyzes individual flags within the `OrchestratorState`.
2. **Sequential Delegation:** 
   * If `flight_options` or `hotel_options` are unpopulated, control moves to the **Planner**.
   * If logistics are resolved but `route_by_day` is empty, control moves to the **Guide**.
   * If itinerary structures are parsed but `total_cost` equals zero, control moves to the **Budget Estimator**.
3. **State Synthesis:** Every agent returns state-specific updates containing specialized data types (e.g., matching dictionary objects or itemized lists). These keys are aggregated using explicit replacement reducers to avoid graph synchronization errors.
4. **Resolution:** Once all data states return valid structures, the workflow hits the `__end__` state and successfully safely exits.

---

## Final Output and Technical Deliverables

When the execution loop completes, the system provides several key technical results:

* **Centralized Verified State:** A unified datastore mapping raw data blocks directly into application parameters without losing unstructured conversational history.
* **Deterministic Financial Analysis:** A conclusive statement regarding financial viability, calculated via external code execution rather than LLM token guessing.
* **Compiled Markdown Manifest:** The system produces a structured documentation manifest mapping flight metrics, hotel rates, and chronologically organized sightseeing parameters directly onto a local storage volume (`final_travel_plan.md`).
