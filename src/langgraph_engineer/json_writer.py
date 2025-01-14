from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
from typing import TypedDict
from langchain_core.messages import RemoveMessage
import json

writer_prompt = """
Write in json format the information you have about the people selected.
you need to include: 
- from 'messages''content': full_name, job_title, company, about, profile_id, linkedin_url, profile_image_url.
- from 'people': "additional_information"

rememeber, consider only the people of interest as intructed by the user.

Dont say anything else. just provide the json in a single codeblock

"""


class Build_data_base(TypedDict):
    data_base: str


def json_writer(state: AgentState, config):
    messages = [
       {"role": "system", "content": writer_prompt}
   ] + state['messages']
    model = _get_model(config, "openai-mini", "report_writer").bind_tools([Build_data_base])
    response = model.invoke(messages)

    data_base = response

    return {"data_base": [data_base]}
