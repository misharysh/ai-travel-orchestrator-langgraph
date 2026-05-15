from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

python_repl_instance = PythonREPL()

# first tool of 'Budget Estimator' agent - calculate trip budget
@tool
def calculate_trip_budget(python_code: str):
    """
    execute Python code to perform precise mathematical calculations for the travel budget.
    use this tool to sum up flight costs, hotel prices per night multiplied by the number of days, and any extra expenses.
    python_code: A valid python code string that prints the final total cost. e.g 'print(350 + (85 * 5))'.
    """

    try:
        result = python_repl_instance.run(python_code)
        return result.strip()
    except Exception as e:
        return f"Error executing calculation: {str(e)}"