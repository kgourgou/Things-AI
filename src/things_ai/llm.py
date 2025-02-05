import dspy


class TaskDetector(dspy.Signature):
    """
    You will be given a text describing a user's todo. Your job is to look
    at what is written after the command sign and identify what the user
    wants you to from the given categories.

    - If the command sign is not present in the text, return an dictionary.
    - If you want to update the date, the date should be in the format "YYYY-MM-DD".

    In the below examples we assume the command sign is "#".

    Example:
    today: "2022-12-31"
    text: "I need to get milk <command_sign> today at 4pm"
    Response:
    title: "I need to get milk"
    due: "2022-12-31 at 4pm"
    append_notes: ""
    tags: []

    Example:
    today: "2022-12-31"
    text: "I need to get this done <command_sign> set the important tag, set the date to tomorrow at 2pm"
    Response:
    title: "I need to get this done"
    tags: ["important"]
    due: "2023-01-01 at 2pm"
    append_notes: ""

     Example:
    today: "2022-12-31"
    text: "I need to get this done <command_sign> set the date to tomorrow at 2pm"
    Response:
    title: "I need to get this done"
    tags: ""
    due: "2023-01-01 at 2pm"
    append_notes: ""

    Please return the output fields
    """

    today: str = dspy.InputField(desc="Today's date in the format 'YYYY-MM-DD'")
    command_sign: str = dspy.InputField(
        desc="The command sign that is used to separate the command from the task."
    )
    text: str = dspy.InputField(desc="The text that you need to analyze.")
    title: str = dspy.OutputField(desc="The new title for the task.")
    append_notes: str = dspy.OutputField(desc="Any new notes to append to the task.")
    due: str = dspy.OutputField(desc="The new date (and possible time) for the task.")
    tags: list[str] = dspy.OutputField(desc="The new tags for the task.")
