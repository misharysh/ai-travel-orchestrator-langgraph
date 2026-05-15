from typing import Literal
from .state import OrchestratorState

# create router
def travel_router(state: OrchestratorState) -> Literal["orchestrator", "planner", "guide", "budget", "__end__"]:
    """routes the execution to the next node based on next_agent field"""

    next_agent = state["next_agent"] if "next_agent" in state and state["next_agent"] else "orchestrator"
    task_complete = state["task_complete"] if "task_complete" in state else False

    print(f"Routing path to -> {next_agent}")

    if next_agent == "end" or task_complete:
        return "__end__"

    if next_agent in ["orchestrator", "planner", "guide", "budget"]:
        return next_agent

    return "orchestrator"