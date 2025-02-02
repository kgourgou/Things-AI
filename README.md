# Unofficial LLM support for the Things 3 todo app

- [Unofficial LLM support for the Things 3 todo app](#unofficial-llm-support-for-the-things-3-todo-app)
  - [Installation](#installation)
  - [Acknowledgements](#acknowledgements)
  - [Risks](#risks)

An experiment in giving LLM support to the Things 3 todo app.

Say you write a task in things like this:

```markdown
I need to do the thing # set tag to hard, due in three days
```

If you then run main.py (and everything goes well), it should update the task in Things 3 to have the tag "hard" and a due date three days from now. It all depends on how up-to-date the SQL database that stores the todos is, and how well the parser works.

You can change the "#" to a different character in the main.py file.

For now, the parser can only update the following fields:

- title
- tags
- due date
- append_notes

Now I'm not a SWE and don't know a lot about how syncing works for Things, but I could imagine someone writing a todo on their phone while having this script running on their computer. It could be a fun way to automate some of the more tedious parts of task management.

## Installation

```bash
pip install uv 
uv pip install -r pyproject.toml
```

You will also need an LLM and Things 3 app installed on your Mac. To connect to the LLM, you need to create a .env file in the root directory with the following content:

```bash
THINGS_AUTH_TOKEN=your_things_auth_token
API_BASE = <API_BASE_URL>
API_KEY = <API_KEY>
MODEL_NAME = <MODEL_NAME>
```

You can learn more about the auth token and the Things URL scheme [here](https://culturedcode.com/things/support/articles/2803573). 

I'm using litellm here, so you can connect to any litellm-supported LLM. I'm using "mradermacher/Bespoke-Stratos-7B-i1-GGUF" from [Bespoke Labs](https://www.bespokelabs.ai/) which I'm running on my laptop with LM-Studio.

## Acknowledgements

This experiment would not have been possible without:

- The [Cultured Code](https://culturedcode.com/things/) team and their URL scheme.
- The [things.py](https://github.com/thingsapi/things.py?tab=readme-ov-file) python library for reading the SQL database.  
- The [json-repair](https://github.com/mangiucugna/json_repair) python library for fixing the output of the LLM.
  
## Risks

- The LLM may overwrite your tasks in ways you don't like. That's why by default I set the possible_edits to be ["tags", "due date", "append_notes"]. You can change this in the main.py file.
