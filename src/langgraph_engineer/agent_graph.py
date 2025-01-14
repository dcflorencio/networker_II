from typing import Literal

from langgraph.graph import StateGraph, END, MessagesState
from langchain_core.messages import AIMessage

from langgraph.prebuilt import ToolNode

import sys

# Add the path to your module directory
# sys.path.append("C:/BCKUP_T440/Pessoal/00_Berkeley/Langgraph/langgraph-networker/src")



from langgraph_engineer.api_call_builder import api_call_builder, fetch_linkedin_data
from langgraph_engineer.conversation_analyzer import analyze_conversation
from langgraph_engineer.state import AgentState, OutputState, GraphConfig
from langgraph_engineer.report_writer import report_writer
from langgraph_engineer.json_writer import json_writer
from langgraph_engineer.report_saver import report_saver
from langgraph_engineer.json_saver import json_saver
from langgraph_engineer.analyze_api_retrived import api_data_analyzer


# def route_critique(state: AgentState) -> Literal["draft_answer", END]:
#     if state['accepted']:
#         return END
#     else:
#         return "draft_answer"

# def route_check(state: AgentState) -> Literal["critique", "draft_answer"]:
#     if isinstance(state['messages'][-1], AIMessage):
#         return "critique"
#     else:
#         return "draft_answer"


def route_start(state: AgentState) -> Literal["report_writer", "analyze_conversation"]:
    if state.get('people'):
        return "report_writer"
    else:
        return "analyze_conversation"


def route_gather(state: AgentState) -> Literal["api_call_builder", END]:
    if state.get('people'):
        return "api_call_builder"
    else:
        return END
    
def route_gather_2(state: AgentState) -> Literal["report_writer", END]:
    if state.get('api_data'):
        return "report_writer"
    else:
        return END


# Define a new graph
workflow = StateGraph(AgentState, input=MessagesState, output=OutputState, config_schema=GraphConfig)
workflow.add_node(analyze_conversation)
workflow.add_node(api_call_builder)
workflow.add_node("Api Call", ToolNode([fetch_linkedin_data]))
workflow.add_node(api_data_analyzer)
workflow.add_node(report_writer)
workflow.add_node(json_writer)
workflow.add_node(report_saver)
workflow.add_node(json_saver)


workflow.set_conditional_entry_point(route_start)

# workflow.add_conditional_edges("analyze_conversation", route_gather)

workflow.add_edge("analyze_conversation", "api_call_builder")

# workflow.add_edge("analyze_conversation", )

workflow.add_edge("api_call_builder", "Api Call")

workflow.add_edge("Api Call", "api_data_analyzer")

# workflow.add_edge("api_data_analyzer", "report_writer")

workflow.add_conditional_edges("api_data_analyzer", route_gather_2)
workflow.add_edge("report_writer", "json_writer")

workflow.add_edge("report_writer", "report_saver")
workflow.add_edge("json_writer", "json_saver")
workflow.add_edge("report_saver", END)
workflow.add_edge("json_saver", END)

graph = workflow.compile()
