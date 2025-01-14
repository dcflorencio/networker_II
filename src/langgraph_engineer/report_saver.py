from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
from typing import TypedDict
from langchain_core.messages import RemoveMessage
import os

def report_saver(state: AgentState, config):
    messages =  state['report'][0]

    file_name = "linkedIN_report.md"
    
    # Save the file in the current path
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(messages)
    