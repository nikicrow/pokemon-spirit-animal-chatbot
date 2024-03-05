import requests
from langchain.tools import tool
from pydantic import BaseModel, Field
import datetime
import wikipedia

# Tool to get the different types of pokemon
@tool
def get_types():
    """Fetch Pokemon types"""
    # api url
    url = "https://api.pokemontcg.io/v2/types"
    payload = {}
    headers = {}

    # call api
    response = requests.request("GET", url, headers=headers, data=payload)

    return response


@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)

# Define the input schema
# class OpenMeteoInput(BaseModel):
#     latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
#     longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

# @tool(args_schema=OpenMeteoInput)
# def get_current_temperature(latitude: float, longitude: float) -> dict:
#     """Fetch current temperature for given coordinates."""
    
#     BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
#     # Parameters for the request
#     params = {
#         'latitude': latitude,
#         'longitude': longitude,
#         'hourly': 'temperature_2m',
#         'forecast_days': 1,
#     }

#     # Make the request
#     response = requests.get(BASE_URL, params=params)
    
#     if response.status_code == 200:
#         results = response.json()
#     else:
#         raise Exception(f"API Request failed with status code: {response.status_code}")

#     current_utc_time = datetime.datetime.utcnow()
#     time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in results['hourly']['time']]
#     temperature_list = results['hourly']['temperature_2m']
    
#     closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
#     current_temperature = temperature_list[closest_time_index]
    
#     return f'The current temperature is {current_temperature}°C'