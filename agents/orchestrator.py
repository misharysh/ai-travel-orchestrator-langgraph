from typing import Dict
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from graph.models import llm
from graph.state import OrchestratorState


def create_orchestrator_chain(llm_model):
    """Creates the orchestrator decision chain for travel planning"""
    orchestrator_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Travel Orchestrator managing a specialized team.
        Decide who goes next based on the current context.
        Respond with ONLY the agent name: planner, guide, budget, or DONE."""),
        ("human", "{task}")
    ])
    return orchestrator_prompt | llm_model


def orchestrator_agent(state: OrchestratorState) -> Dict:
    task = state["current_task_from_human"] if "current_task_from_human" in state and state["current_task_from_human"] else "No task provided"

    has_flights = bool(state["flight_options"]) if "flight_options" in state else False
    has_hotels = bool(state["hotel_options"]) if "hotel_options" in state else False
    has_cultural_program = bool(state["route_by_day"]) if "route_by_day" in state else False

    total_cost = state["total_cost"] if "total_cost" in state else 0.0
    has_total_cost = total_cost > 0

    # request to model
    chain = create_orchestrator_chain(llm)
    decision = chain.invoke({"task": task})

    decision_text = decision.content.strip().lower()
    print(f"JUST FOR DEBUG: Orchestrator chose {decision_text}")

    if has_total_cost:
        next_agent = "end"
        orchestrator_message = "Orchestrator: all tasks complete! finalizing the travel plan."
        task_complete = True
    elif not has_flights or not has_hotels:
        next_agent = "planner"
        orchestrator_message = "Orchestrator: let's find logistics. assigning to travel planner."
        task_complete = False
    elif not has_cultural_program:
        next_agent = "guide"
        orchestrator_message = "Orchestrator: logistics ready. time for the cultural program. assigning to guide..."
        task_complete = False
    elif not has_total_cost:
        next_agent = "budget"
        orchestrator_message = "Orchestrator: plan is ready. calculating total budget. assigning to budget estimator..."
        task_complete = False
    else:
        next_agent = "end"
        orchestrator_message = "Orchestrator: task finished."
        task_complete = True

    return {
        "messages": [AIMessage(content=orchestrator_message)],
        "next_agent": next_agent,
        "task_complete": task_complete
    }
