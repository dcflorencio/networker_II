from langgraph.graph import MessagesState
from typing import TypedDict, Literal
class AgentState(MessagesState):
    people: str
    code: str
    accepted: bool
    report: str
    api_data: str
    data_base: str


class OutputState(TypedDict):
    code: str


class GraphConfig(TypedDict):
    gather_model: Literal['openai', 'openai-mini', 'anthropic']
    api_call_builder: Literal['openai', 'openai-mini', 'anthropic']
    writer: Literal['openai', 'openai-mini', 'anthropic']
    report_writer: Literal['openai', 'openai-mini', 'anthropic']
    report_saver: Literal['openai', 'openai-mini', 'anthropic']
