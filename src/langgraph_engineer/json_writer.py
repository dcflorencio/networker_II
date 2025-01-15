from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
from typing import TypedDict
from langchain_core.messages import RemoveMessage
import json

writer_prompt = """
Write in json format the information you have about the people selected.
you need to include: 
- from the api call that was made: full_name, job_title, company, about, profile_id, linkedin_url, profile_image_url.
- from 'people': "personal_information"

rememeber, consider only the people of interest as intructed by the user.


Dont say anything else. just provide the json in a single codeblock

"""


class Build_database(TypedDict):
    database: str


def json_writer(state: AgentState, config):
    messages = [
       {"role": "system", "content": writer_prompt}, 
       {"role": "user", "content": state.get('people')}
   ] + state['messages']
    model = _get_model(config, "openai-mini", "report_writer").bind_tools([Build_database])
    response = model.invoke(messages)

    database = response

    return {"data_base": [database]}



# Extract the following fields for the selected individuals:
# - "full_name"
# - "job_title"
# - "company"
# - "about"
# - "profile_id"
# - "linkedin_url"
# - "profile_image_url"
# - "personal_information" (from the "people" key).

# Use the "people" key to find the "personal_information" field. Match individuals by their "name" or "id" field. Include "personal_information" for only the selected individuals. If "personal_information" is unavailable, set it to "Not available".

# For example:
# {
#     "full_name": "John doe",
#     "job_title": "Software Engineer",
#     "company": "Salesforce",
#     "about": "Not available",
#     "profile_id": "Not available",
#     "linkedin_url": "Not available",
#     "profile_image_url": "Not available",
#     "personal_information": "Works on optimizing platforms for scalability and performance; interested in AI; enjoys photography."
# }

# dont make up information that does that exist in the context!!

# if you dont know return "N/A" for the field