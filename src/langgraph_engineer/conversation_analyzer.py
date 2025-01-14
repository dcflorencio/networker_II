from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
from typing import TypedDict
from langchain_core.messages import RemoveMessage

conversation_analyzer_prompt = """
Your task is to analyze the dialogue and extract details about each individual mentioned in the conversation.
Your response must be in JSON format, with the following fields for each person:

id: A unique, incremental identifier for each person. Do not include the same person more than once.
name: The person’s name.
company_name: The name of the company where the person works.
job_title: The person’s job title.
location: The place where the person lives or works.
additional_information: Relevant details about the person, such as their interests, hobbies, number of children, place of birth, 
or any other significant facts mentioned in the conversation.

Your response should be formatted as a single JSON object containing an array of these records.
The goal is to build a comprehensive database of individuals for networking purposes.
Ensure accuracy and completeness without duplicating entries for the same person.


Once you are done confirm readiness to proceed with generating the database.

"""


class Build(TypedDict):
    people: str


def analyze_conversation(state: AgentState, config):
    messages = [
       {"role": "system", "content": conversation_analyzer_prompt}
   ] + state['messages']
    model = _get_model(config, "openai-mini", "conversation_analyzer_model").bind_tools([Build])
    response = model.invoke(messages)
    if len(response.tool_calls) == 0:
        return {"messages": [response]}
    else:
        people = response.tool_calls[0]['args']['people']
        delete_messages = [RemoveMessage(id=m.id) for m in state['messages']]
        return {"people": people, "messages": delete_messages}
