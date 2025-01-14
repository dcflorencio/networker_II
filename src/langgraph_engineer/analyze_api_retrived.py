from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
from typing import TypedDict


table_prompt = """


write in a json structure, for each tool call, cointaning: id(incremental), full_name, company for every person.

ask the user for feedback on which persons from the table they are interested in.

once you are satisfied, return the full data from the tool for that person or persons th user selected.

"""


class Build_api_data(TypedDict):
    api_data: str


def api_data_analyzer(state: AgentState, config):
    messages = [
       {"role": "system", "content": table_prompt}
   ] + state['messages']
    model = _get_model(config, "openai-mini", "report_writer").bind_tools([Build_api_data])
    response = model.invoke(messages)

    api_data = response

    # return {"api_data": [api_data]}

    return {"messages": [response]}

    # if len(response.tool_calls) == 0:
    #     return {"messages": [response]}
    # else:
    #     api_data = response.tool_calls[0]['args']['api_data']
        
    #     return {"api_data": [api_data]}