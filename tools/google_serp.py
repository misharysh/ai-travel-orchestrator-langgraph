import os
from langchain_core.tools import tool
from serpapi import GoogleSearch

# serpApi (Google)
SERPAPI_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")

# first tool of 'Travel Planner' agent - search flights
@tool
def search_flights_google(departure_id: str, arrival_id: str, outbound_date: str, return_date: str = None):
    """
    Search for real-time flights prices using Google Search API via SerpApi.
    departure_id: IATA(International Air Transport Association) code of departure city/airport (e.g. 'ROM').
    arrival_id: IATA(International Air Transport Association) code of arrival city/airport (e.g. 'PAR').
    outbound_date: flight date in YYYY-MM-DD format.
    return_date: optional return flight date in YYYY-MM-DD format.
    """

    #reserve flights
    mock_flights = [
        {"airline": "Lufthansa", "flight_number": "LH232", "price": 350, "duration": 120, "type": "best_option"},
        {"airline": "Ryanair", "flight_number": "FR4342", "price": 180, "duration": 135, "type": "best_option"}
    ]

    # Google Flights API
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "api_key": SERPAPI_KEY,
        "currency": "USD",
        "hl": "en"
    }

    if return_date:
        params["return_date"] = return_date

    try:
        search = GoogleSearch(params)
        result = search.get_dict()

        flights = result.get("best_flights", [])

        if not flights:
            print("SERP_API: Google Flights returned 0 results. Using realistic Mock Data to prevent loop.")

            return mock_flights

        simplified_flights = []
        for flight in flights[:3]:
            legs = flight.get("flights", [])
            first_leg = legs[0] if isinstance(legs, list) and len(legs) > 0 else {}

            simplified_flights.append({
                "airline": first_leg.get("airline", "Unknown Airline"),
                "flight_number": first_leg.get("flight_number", "N/A"),
                "price": flight.get("price",250),
                "duration": flight.get("total_duration", 120),
                "type": "best_option"
            })

        return simplified_flights

    except Exception as e:
        print(f"SERP_API Flight Error: {e}. Falling back to Mock Data.")

        return mock_flights

# second tool of 'Travel Planner' agent - search hotels
@tool
def search_hotels_google(q: str, check_in_date:str, check_out_date: str):
    """
    Search for hotels using Google Search API via SerpApi.
    q: the destination of city name (e.g. Rimini).
    check_in_date: check-in date in YYYY-MM-DD format.
    check_out_date: check-out date in YYYY-MM-DD format.
    """

    # reserve data
    mock_hotels = [
        {"name": "Hotel Roma Central", "price": 95, "rating": 4.5, "reviews": 120, "link": ""},
        {"name": "Colosseum View Suite", "price": 130, "rating": 4.8, "reviews": 85, "link": ""}
    ]

    # Google hotels API
    params = {
        "engine": "google_hotels",
        "q": q,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "api_key": SERPAPI_KEY,
        "currency": "USD",
        "hl": "en"
    }

    try:
        search = GoogleSearch(params)
        result = search.get_dict()

        hotels = result.get("properties", [])

        if not hotels:
            print("SERP_API: Google Hotels returned 0 results. Using realistic Mock Data to prevent loop.")

            return mock_hotels

        simplified_hotels = []
        for hotel in hotels[:3]:
            simplified_hotels.append({
                "name": hotel.get("name", "Unknown Hotel"),
                "price": hotel.get("rate_per_night", {}).get("lowest") if hotel.get("rate_per_night") else "N/A",
                "rating": hotel.get("overall_rating", "N/A"),
                "reviews": hotel.get("reviews_count", 0),
                "link": hotel.get("link", "")
            })

        return simplified_hotels

    except Exception as e:
        print(f"SERP_API Hotel Error: {e}. Falling back to Mock Data.")

        return mock_hotels