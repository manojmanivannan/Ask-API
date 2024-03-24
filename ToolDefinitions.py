import requests
import json
from langchain.agents import Tool

def fetch_crime_record_stats(json_request: str="{}"):
    url = 'http://localhost:8080/'
    endpoint = 'crime_statistics'
    arguments = json.loads(json_request)
    date = arguments.get('date',None)
    r = requests.get(url + endpoint, params={'date': date})
    return r.content

def fetch_crime_records(json_request: str):
    url = 'http://localhost:8080/'
    endpoint = 'search_crime_records'
    arguments = json.loads(json_request)
    location = arguments.get('location',None)
    crime_type = arguments.get('crime_type',None)
    date = arguments.get('date',None)
    r = requests.get(url + endpoint, params={'location': location, 'crime_type': crime_type})
    return r.content




fetch_crime_record_stats_tool = Tool(
    name="Get crime database stats from /statistics endpoint - tool/API",
    func=fetch_crime_record_stats,
    description="""Fetches statistics from crime records database using API endpoints,
    input should be a JSON string which is optional""",
    handle_tool_error=True
)
fetch_crime_records_tool = Tool(
    name="Get Crime record by location or crime type or date using /search_crime_records endpoint - tool/API",
    func=fetch_crime_records,
    description="""Fetches the crime records based on location or crime type or both using API endpoints,
    input should be a JSON string with location and crime_type as keys""",
    handle_tool_error=True
)
