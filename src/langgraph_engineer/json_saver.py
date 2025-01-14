from langgraph_engineer.model import _get_model
from langgraph_engineer.state import AgentState
import os
import json

def json_saver(state: AgentState, config):
    # Extract the first item from the data_base
    messages = state["data_base"][0]

    # Parse the object into a serializable format using custom parsing
    def convert_to_serializable(obj):
        """Convert objects like AIMessage to a serializable format."""
        if hasattr(obj, "to_dict"):
            return obj.to_dict()  # Convert to dictionary if `to_dict` method exists
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]  # Recursively handle lists
        elif isinstance(obj, dict):
            return {key: convert_to_serializable(value) for key, value in obj.items()}  # Recursively handle dicts
        elif hasattr(obj, "__dict__"):
            return obj.__dict__  # Convert object's attributes to a dictionary
        return str(obj)  # Fallback: Convert to string

    # Convert the `messages` object into a serializable format
    serializable_messages = convert_to_serializable(messages)

    # Save the serialized messages to a temporary JSON file
    temp_file_path = "data_base.json"
    with open(temp_file_path, "w", encoding="utf-8") as temp_file:
        json_text = json.dumps(serializable_messages, indent=4, ensure_ascii=False)
        temp_file.write(json_text)  # Write the formatted JSON string

    # Open the temporary file, extract the 'content' key, and save it
    with open(temp_file_path, "r", encoding="utf-8") as temp_file:
        saved_data = json.load(temp_file)  # Load the temporary JSON data

    # Extract only the 'content' key
    content_only = saved_data.get("content", None)

    if content_only:
        # Remove Markdown code block markers if present
        if content_only.startswith("```json\n") and content_only.endswith("\n```"):
            content_only = content_only[8:-4]  # Strip Markdown markers
        try:
            content_only = json.loads(content_only)  # Parse as JSON
        except json.JSONDecodeError:
            pass  # Keep as string if it's not valid JSON

        # Save the content-only data to a new file
        content_file_path = "content_only.json"
        with open(content_file_path, "w", encoding="utf-8") as content_file:
            json.dump(content_only, content_file, indent=4, ensure_ascii=False)

        print(f"Content successfully saved to {content_file_path}.")
    else:
        print("No 'content' key found in the saved data.")

    # Delete the temporary file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(f"Temporary file {temp_file_path} deleted.")
    else:
        print(f"Temporary file {temp_file_path} not found.")
