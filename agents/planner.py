from graph.state import OrchestratorState
from tools.google_serp import search_flights_google, search_hotels_google
from graph.models import llm
from typing import Dict
from langchain_core.messages import AIMessage

def travel_planner_agent(state: OrchestratorState) -> Dict:
    """Travel planner searches for both: flights and hotels"""

    task = state["current_task_from_human"] if "current_task_from_human" in state and state["current_task_from_human"] else "No task provided"

    planner_llm = llm.bind_tools([search_flights_google,search_hotels_google])

    planner_prompt = f"""
    you are professional travel agent. based on this request {task}.
    YOUR GOAL: 
    1. Call `search_flights_google` with EXACTLY these arguments: departure_id, arrival_id, outbound_date, return_date. Do NOT invent other parameters like max_price or budget.
    2. Call `search_hotels_google` with EXACTLY these arguments: q, check_in_date, check_out_date.
    
    Always use airport codes for flights (e.g. ROM, PAR) and city names for hotels.
    Dates must be YYYY-MM-DD.
    """

    response = planner_llm.invoke(planner_prompt)

    flights_data = []
    hotels_data = []

    if hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("args", {})

            clean_args = {k: v for k, v in tool_args.items() if k in ['departure_id', 'arrival_id', 'outbound_date', 'return_date', 'q', 'check_in_date', 'check_out_date']}

            if tool_name == "search_flights_google":
                print(f"PLANNER: Executing flight search with args: {clean_args}")
                result = search_flights_google.invoke(clean_args)

                if isinstance(result, list):
                    flights_data.extend(result)

            elif tool_name == "search_hotels_google":
                print(f"PLANNER: executing hotel search with args: {clean_args}")
                result = search_hotels_google.invoke(clean_args)
                if isinstance(result, list):
                    hotels_data.extend(result)

    agent_message = "Travel Planner - found flights and hotel options."

    return {
        "messages": [response, AIMessage(content=agent_message)],
        "flight_options": flights_data,
        "hotel_options": hotels_data,
        "next_agent": "orchestrator"
    }