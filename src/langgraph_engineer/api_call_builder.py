from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState

from typing import TypedDict
from langchain_core.messages import RemoveMessage
import os
from typing import Any, Dict
import http.client


rapidapi_key = os.getenv("RAPIDAPI_KEY")

prompt = """
you are tasked to make an api call using fetch_linkedin_data to get professional information on people.

Function to query LinkedIn API.
Here are the parameters for the API:

{
  "Parameters": {
    "payload": {
      "type": "str",
      "description": "A JSON-formatted string containing the search parameters for the API.",
      "keys": {
        "name": {
          "type": "str",
          "description": "The full name of the person to search for."
        },
        "company_name": {
          "type": "str",
          "description": "The company where the person works (optional)."
        },
        "job_title": {
          "type": "str",
          "description": "The job title of the person (optional)."
        },
        "location": {
          "type": "str",
          "description": "The geographical location of the person (e.g., 'US')."
        },
        "keywords": {
          "type": "str",
          "description": "Additional keywords to refine the search (optional)."
        },
        "limit": {
          "type": "int",
          "description": "The maximum number of profiles to retrieve. ALWAYS 5"
        }
      }
    }
  }
}


"""


def fetch_linkedin_data(name: str, company_name: str = "", job_title: str = "", location: str = "", 
                        keywords: str = "", limit: int = 5) -> Dict[str, Any]:
    """
    Function to query the Fresh LinkedIn Profile Data API.
    
    :param name: The full name of the person to search for.
    :param company_name: The company where the person works (optional).
    :param job_title: The job title of the person (optional).
    :param location: The geographical location of the person (e.g., "US").
    :param keywords: Additional keywords to refine the search (optional).
    :param limit: The maximum number of profiles to retrieve (default: 5).
    
    :return: A dictionary containing the API response, including status, reason, and data.
    """
    
    # API endpoint and connection setup
    conn = http.client.HTTPSConnection("fresh-linkedin-profile-data.p.rapidapi.com")

    # Local variable for API key
    headers = {
        'x-rapidapi-key': rapidapi_key,  # Replace `rapidapi_key` with your local variable
        'x-rapidapi-host': "fresh-linkedin-profile-data.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    # Create the JSON payload
    payload = {
        "name": name,
        "company_name": company_name,
        "job_title": job_title,
        "location": location,
        "keywords": keywords,
        "limit": limit
    }

    # Convert payload to JSON string
    import json
    payload_json = json.dumps(payload)

    # Send the POST request
    conn.request("POST", "/google-full-profiles", payload_json, headers)

    # Get the API response
    response = conn.getresponse()
    data = response.read()

    # Decode and return the response
    return {
        "status": response.status,
        "reason": response.reason,
        "data": data.decode("utf-8")
    }





def api_call_builder(state: AgentState, config):
    messages = [
       {"role": "system", "content": prompt}, 
       {"role": "user", "content": state.get('people')}
   ] + state['messages']
    model = _get_model(config, "openai-mini", "api_call_builder").bind_tools([fetch_linkedin_data])
    response = model.invoke(messages)
    if len(response.tool_calls) == 0:
        return {"messages": [response]}
    else:

        return {"messages": [response]}

