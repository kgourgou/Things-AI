import os
import time
from things_ai import ThingsAI
from dotenv import load_dotenv
import dspy
from loguru import logger

load_dotenv(".env.things")

TIME_TO_WAIT = 0.1  # minutes

lm = dspy.LM(
    model=os.getenv("MODEL_NAME"),
    api_key=os.getenv("API_KEY"),
    api_base=os.getenv("API_BASE"),
    cache=False,
)

dspy.configure(lm=lm)
th = ThingsAI()

# This will fetch tasks from Things from the last 20 days and update them based on the command sign.
# anything after the command sign will be considered a command for the LLM.
# for safety we never update the title of the task,
# but you may add it here if you like.
while True:
    logger.info("Scanning tasks...")
    th(last="20d", command_sign=";", possible_edits=["due", "tags", "append_notes"])
    time.sleep(TIME_TO_WAIT * 60)  # Convert minutes to seconds
