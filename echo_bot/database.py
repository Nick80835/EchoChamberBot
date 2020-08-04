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
