from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
from typing import TypedDict
from langchain_core.messages import RemoveMessage

writer_prompt = """
Write a detailed report on the people. make it in markdown format.
The report should have a row for each person and tthe following columns:
Full name, job title, company, about, linkedin url, the picture in a small format
"""


class Build_write(TypedDict):
    report: str


def report_writer(state: AgentState, config):
    messages = [
       {"role": "system", "content": writer_prompt}
   ] + state['messages']
    model = _get_model(config, "openai-mini", "report_writer").bind_tools([Build_write])
    response = model.invoke(messages)

    report = response.tool_calls[0]['args']['report']

    return {"report": [report]}
