from .router import travel_router
from .state import OrchestratorState
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from agents.orchestrator import orchestrator_agent
from agents.planner import travel_planner_agent
from agents.guide import guide_agent
from agents.budget import budget_estimator_agent

# create workflow
workflow = StateGraph(OrchestratorState)

# create nodes
workflow.add_node("orchestrator", orchestrator_agent)
workflow.add_node("planner", travel_planner_agent)
workflow.add_node("guide", guide_agent)
workflow.add_node("budget", budget_estimator_agent)

# entry point
workflow.set_entry_point("orchestrator")

# set edges
for node_name in ["orchestrator", "planner", "guide", "budget"]:
    workflow.add_conditional_edges(
        node_name,
        travel_router, # decides how to route
        {
            "orchestrator": "orchestrator",
            "planner": "planner",
            "guide": "guide",
            "budget": "budget",
            "__end__": "__end__"
        }
    )

memory = MemorySaver()

# compile our graph
travel_assistant_graph = workflow.compile(checkpointer=memory)