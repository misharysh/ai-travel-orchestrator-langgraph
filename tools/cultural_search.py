import os
from langchain_core.tools import tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools.tavily_search import TavilySearchResults


# first tool of 'Guide' agent - search historical facts about the concrete city
@tool
def search_cultural_program_wikipedia(query: str):
    """
    Search Wikipedia for cultural information, historical landmarks,
    and top sightseeing locations about a specific city or destination.
    query: The name of the city or attraction to look up (e.g., 'Rome', 'Colosseum').
    """
    import wikipedia
    wikipedia.set_user_agent("MyAIApp/1.0 (contact@example.com)")

    api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=800)
    wiki = WikipediaQueryRun(api_wrapper=api_wrapper_wiki, description="Query wiki")

    try:
        result = wiki.invoke({"query": query})

        return result

    except Exception as e:

        return f"Error searching Wikipedia: {str(e)}"

# second tool of 'Guide' agent - search cultural program for the concrete city
@tool
def search_cultural_program_tavily(query: str):
    """
    Search the live web via Tavily to find current events, festivals, local entertainment, and fresh travel recommendations for a specific city.
    query: The search query combining city and target events (e.g., 'Rome events June 2026', 'best restaurants in Paris').
    """
    if not os.getenv("TAVILY_API_KEY"):
        return "Error: TAVILY_API_KEY is missing in your environment variables."

    tavily = TavilySearchResults(max_results=2)

    try:
        result = tavily.invoke({"query": query})

        return result

    except Exception as e:

        return f"Error searching Tavily: {str(e)}"