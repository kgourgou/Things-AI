import webbrowser

THINGS_BASE_URL = "things:///"


class ThingsWriter:
    def __init__(self, things_auth_token: str):
        self.things_auth_token = things_auth_token

    def update_entry(
        self,
        uuid: str,
        title: str | None = None,
        append_notes: str | None = None,
        due: str | None = None,
        tags: list[str] | None = None,
    ):
        """
        Use the Things URL scheme to update a specific task.

        Args:
            uuid (str): The ID of the task.
            title (str): The title of the task.
            append_notes (str): The notes to append to the task.
            due (str): The date to set for the task.
            tags (list[str]): The tags to set for the task
        """
        # build the URL
        base_url = f"{THINGS_BASE_URL}update?"

        base_url += f"auth-token={self.things_auth_token}&"
        base_url += f"id={uuid}&"

        if title:
            base_url += f"title={title}&"

        if append_notes:
            base_url += f"append-notes={append_notes}&"

        # due should be a date, i.e., "2022-12-31"
        if due:
            base_url += f"when={due}&"

        if tags:
            base_url += "%2C%20".join(tags)

        webbrowser.open(base_url)
