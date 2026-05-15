from langgraph.graph import MessagesState
from typing import List, Dict, Annotated

def replace_list(old: list, new: list) -> list:
    return new if new else old

def replace_dict(old: dict, new: dict) -> dict:
    return new if new else old

class OrchestratorState(MessagesState):
    """State for langgraph multi-agent system"""

    # general fields
    next_agent: str = ""
    task_complete: bool = False
    current_task_from_human: str = "" # "Rome, 5 days, start from June 5, 1000$ - budget"
    final_report: str = ""

    # fields from 'TravelPlanner' agent
    flight_options: Annotated[List[Dict], replace_list] = []
    hotel_options: Annotated[List[Dict], replace_list] = []

    # fields from 'Guide' agent
    route_by_day: Annotated[dict, replace_dict] = {}
    interesting_facts: str = ""

    # fields from 'BudgetEstimator' agent
    total_cost: float = 0.0
    currency: str = "USD"
    budget_status: str = ""