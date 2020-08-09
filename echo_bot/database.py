from io import BytesIO
from random import choice

from sqlitedict import SqliteDict


class Database:
    def __init__(self):
        self.db = SqliteDict("database.sqlite")

        if "echoes" not in self.db.keys():
            self.db["echoes"] = []
            self.db.commit()

    def add_to_echoes(self, echo_text: str):
        if echo_text not in self.db["echoes"]:
            self.db["echoes"] += [echo_text]
            self.db.commit()

    def get_random_echo(self) -> str:
        try:
            return choice(self.db["echoes"])
        except IndexError:
            return "Congrats, that's the first message in my database!"

    def get_stats(self) -> str:
        return f"Message count: {len(self.db['echoes'])}"

    def get_dump(self) -> BytesIO:
        dump_bytes = BytesIO(bytes("\n".join(self.db['echoes']), encoding="utf-8"))
        dump_bytes.name = "dump.txt"
        return dump_bytes

    def overwrite(self, ow_bytes: BytesIO):
        ow_bytes.seek(0)
        ow_list = ow_bytes.read().decode("utf-8").split("\n")
        self.db["echoes"] = ow_list
        self.db.commit()

    def remove_echo(self, echo_text: str) -> str:
        try:
            self.db["echoes"].remove(echo_text)
            self.db.commit()
            return "Successfully removed from my database!"
        except ValueError:
            return "That text isn't in my database!"
