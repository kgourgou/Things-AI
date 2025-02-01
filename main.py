import json
import os
import urllib.parse
from dotenv import load_dotenv
import things
from openai import OpenAI

import loguru

logger = loguru.logger


# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


# Load API Key from .env
load_dotenv(".env.things")
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuration
THINGS_BASE_URL = "things:///"
AUTH_TOKEN = os.getenv(
    "THINGS_AUTH_TOKEN"
)  # Add your Things auth token to the .env file
MODEL_NAME = "lm_studio/mradermacher/Bespoke-Stratos-7B-i1-GGUF"


def fetch_tasks(last="7d") -> list[dict]:
    logger.debug("Fetching tasks from Things...")
    return things.todos(last=last, include_items=True)


def generate_prompt(todo: dict) -> str:
    """
    Generate a prompt to send to the LLM for a single todo.
    """
    prompt = (
        "You are an intelligent assistant reviewing my to-do. Here is the task:\n\n"
    )

    prompt += f"- Task: {todo['title']}\n"
    if todo["notes"]:
        prompt += f"  Notes: {todo['notes']}\n"
    if todo["deadline"]:
        prompt += f"  Deadline: {todo['deadline']}\n"
    prompt += "\n"

    prompt += """Please review this task and provide very concise feedback:

    1. Comment on how it can be made less vague (if it is vague). 
    2. Use the tools provided to link to relevant information. 
    
    Output your suggestions as a JSON object with the format:
    '{"suggestions": {...}}'"""
    return prompt


tools = [
    {
        "type": "function",
        "function": {
            "name": "say_hello",
            "description": "Says hello to someone",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The person's name"}
                },
                "required": ["name"],
            },
        },
    }
]


def say_hello(name):
    return f"Hello, {name}!"


def interact_with_llm(prompt):
    """
    Send the prompt to OpenAI and get the response.
    """

    response = client.chat.completions.create(
        model="mradermacher/Bespoke-Stratos-7B-i1-GGUF",
        messages=[
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        tools=tools,
    )
    import ipdb

    ipdb.set_trace()
    return response["choices"][0]["message"]["content"]


def update_task_in_things(todo_id, title=None, notes=None, deadline=None):
    """
    Use the Things URL scheme to update a specific task.
    """
    base_url = f"{THINGS_BASE_URL}update?"
    params = {
        "id": todo_id,
        "title": title,
        "notes": notes,
        "deadline": deadline,
        "auth-token": AUTH_TOKEN,
    }
    # Filter out None values
    params = {key: value for key, value in params.items() if value}
    query_string = urllib.parse.urlencode(params)
    update_url = base_url + query_string

    print(f"Opening URL to update task: {update_url}")


def process_single_todo(todo: dict):
    """
    Process a single todo item.
    """
    print(f"\nProcessing task: {todo['title']}")

    prompt = generate_prompt(todo)
    print("\nGenerated Prompt:")
    print(prompt)

    print("\nReviewing to-do with LLM...\n")
    response = interact_with_llm(prompt)
    response = response.replace("<|eot_id|>", "")
    print("LLM Response:")
    print(response)

    # Parse the JSON suggestions
    try:
        suggestion = json.loads(response)
        print("\nSuggestions for Task:")
        print(json.dumps(suggestion["suggestions"], indent=4))

        # Update the task in Things based on LLM's suggestions
        title = suggestion["suggestions"].get("title")
        notes = suggestion["suggestions"].get("notes")
        deadline = suggestion["suggestions"].get("deadline")
        update_task_in_things(todo["id"], title=title, notes=notes, deadline=deadline)

    except json.JSONDecodeError:
        print("Error: Could not parse LLM response.")


def main():
    print("Welcome to Things Task Reviewer!")
    todos = fetch_tasks()

    print(f"Found {len(todos)} to-dos.")

    for todo in todos:
        process_single_todo(todo)
        user_input = input("\nPress Enter to continue to next task, or 'q' to quit: ")
        if user_input.lower() == "q":
            break


if __name__ == "__main__":
    main()
