from logging import Logger
from re import search

from echo_bot.database import Database


class CommandHandler:
    pattern_template = "(?is)^/{0}(?: |$)(.*)"
    commands = []

    def __init__(self, database: Database, logger: Logger):
        self.database = database
        self.logger = logger
        self._register_commands()

    def command(self, pattern):
        def decorator(func):
            self.commands.append({
                "pattern": pattern,
                "function": func
            })

            return func
        return decorator

    async def handle_command(self, event):
        for command in self.commands:
            pattern_match = search(self.pattern_template.format(command["pattern"]), event.raw_text)

            if pattern_match:
                if event.is_reply:
                    event.args = (await event.get_reply_message()).raw_text
                else:
                    event.args = pattern_match.groups()[-1]

                self.logger.info(f"Handling command '{command['pattern']}'")
                await command["function"](self, event)

    def _register_commands(self):
        @self.command("stats")
        async def stats_command(self, event):
            await event.reply(self.database.get_stats())

        @self.command("unecho")
        async def unecho_command(self, event):
            await event.reply(self.database.remove_echo(event.args))
