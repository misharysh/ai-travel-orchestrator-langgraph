import re
from typing import Dict
from graph.state import OrchestratorState
from tools.calculator import calculate_trip_budget

def budget_estimator_agent(state: OrchestratorState) -> Dict:
    """budget estimator calculates total trip costs and checks against user budget"""

    from graph.models import llm

    # get our data from state
    task = state["current_task_from_human"] if "current_task_from_human" in state and state["current_task_from_human"] else "No task provided"
    flights = state.get("flight_options", [])
    hotels = state.get("hotel_options", [])

    # bind our tool
    budget_llm = llm.bind_tools([calculate_trip_budget])

    # create prompt
    budget_prompt = f"""
    you are a professional financial estimator for travel planning. user request: {task}
    we have collected the following data:
    - flight options found: {flights}
    - hotel options found: {hotels}

    YOUR GOAL:
    1. determine the flight cost and hotel cost per night from the data.
    2. determine the total number of nights/days from the user request.
    3. generate and call the `calculate_trip_budget` tool with python code to calculate the exact total cost.
       the code must print only the final number (e.g., `print(350 + (100 * 5))`).
    4. compare the total cost with the user's budget limit and provide a verdict.
    """

    # first call of llm
    response = budget_llm.invoke(budget_prompt)

    total_cost = 0.0
    calculation_result = ""

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "calculate_trip_budget":
                calculation_result = calculate_trip_budget.invoke(tool_call["args"])

        # second call of llm - model need to checj result of calculation
        response = budget_llm.invoke(budget_prompt)

    try:
        # check number in response
        clean_cost = re.findall(r"\d+\.?\d*", calculation_result)
        if clean_cost:
            total_cost = float(clean_cost[0])
        else:
            # if model wrote text
            clean_cost_alt = re.findall(r"\d+\.?\d*", response.content)
            if clean_cost_alt:
                total_cost = float(clean_cost_alt[0])
    except Exception as e:
        print(f"Error extracting total cost: {e}")

    user_budget_limit = 1000.0 # by default, just for MVP

    if total_cost <= user_budget_limit:
        budget_status = f"within budget. total: {total_cost} USD (limit: {user_budget_limit} USD)."
    else:
        budget_status = f"budget exceeded! total: {total_cost} USD (limit: {user_budget_limit} USD)."

    agent_message = f"budget estimator finished calculations. status: {budget_status}"

    return {
        "messages": [],
        "total_cost": total_cost,
        "budget_status": budget_status,
        "next_agent": "orchestrator"
    }