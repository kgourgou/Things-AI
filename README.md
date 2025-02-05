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

If you then run main.py (and everything goes well), it should update the task in Things 3 to have the tag "hard" (if that tag already exists) and the due date three days from now.

Essentially you write your tasks as

```markdown
<task title> <command character> <commands to the LLM for updating the task in Things>
```

and when Things cloud brings your tasks to your mac, the script will pick those with commands to the LLM
and update them accordingly, then remove the command from the task. Those tasks will then be synced back to the cloud.

You can change the "#" to a different command character in the main.py file.

For now, the parser can only update the following fields:

- title
- tags
- due date
- append_notes

But in reality it should be simple to support any field that is updateable through the Things URL scheme,
eg. the deadline, the project, the area, checklists, etc.

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

I'm using litellm, so you can connect to any litellm-supported LLM. If you want to use a local model, I recommend either

- "mradermacher/Bespoke-Stratos-7B-i1-GGUF" from [Bespoke Labs](https://www.bespokelabs.ai/)
- or <https://huggingface.co/mlabonne/NeuralBeagle14-7B> from Maxime.

I use those locally with LMStudio and a 4bit quantization for about 5ish GB of RAM usage.

## Acknowledgements

This experiment would not have been possible without:

- The [Cultured Code](https://culturedcode.com/things/) team and their URL scheme.
- The [things.py](https://github.com/thingsapi/things.py?tab=readme-ov-file) python library for reading the Things3 SQL database.

I also appreciate the [DSPy](https://github.com/stanfordnlp/dspy/issues/1539) library and open-source model developers. 
  
## Risks

- The LLM may overwrite your tasks in ways you don't like. That's why by default I set the possible_edits to be ["tags", "due date", "append_notes"]. You can change this in the main.py file.
- I don't know what triggers cloud sync in Things 3, so you may have to wait a bit for the changes to be reflected in the app.
