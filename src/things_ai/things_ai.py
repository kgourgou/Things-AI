import datetime
import os

import dspy
import loguru
import things

from things_ai.llm import TaskDetector
from things_ai.things_writer import ThingsWriter

logger = loguru.logger


class ThingsAI(dspy.Module):
    def __init__(self, things_auth_token: str | None = None):
        self.things_auth_token = things_auth_token or os.getenv("THINGS_AUTH_TOKEN")
        self.writer = ThingsWriter(things_auth_token=self.things_auth_token)
        self.task_detector = dspy.Predict(TaskDetector)

    def forward(
        self,
        last: str = "1d",
        possible_edits: list[str] | None = None,
        command_sign: str = "#",
    ):
        """

        Fetch tasks from Things and update them based on the command sign.

        Args:
            last (str): The time period to fetch tasks from.
            possible_edits (list[str]): The possible edits to make to the tasks.
            command_sign (str): The sign to look for in the task title.
        """

        possible_edits = possible_edits or ["due", "tags", "append_notes"]

        todos = things.todos(last=last, include_items=True)
        logger.info(f"Fetched {len(todos)} tasks from Things.")

        today = datetime.datetime.now()
        today_date = f"{today.strftime('%A')}, {today.strftime('%Y-%m-%d')}"

        for task in todos:
            text = task["title"]

            if command_sign not in text:
                continue

            logger.info(f"Found task to update: {text}")
            response = self.task_detector(
                text=text, command_sign=command_sign, today=today_date
            ).toDict()

            # Filter out anything we don't want to update
            update_dict = {
                key: value for key, value in response.items() if key in possible_edits
            }

            logger.debug(f"Updating task with: {update_dict}")

            if "title" not in update_dict:
                update_dict["title"] = text.split(command_sign)[0].strip()

            if update_dict:
                self.writer.update_entry(uuid=task["uuid"], **update_dict)
