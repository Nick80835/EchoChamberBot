from re import search


class CommandHandler:
    pattern_template = "(?is)^(/|e.){0}(?: |$)(.*)"
    commands = []

    def __init__(self, database, logger, settings):
        self.owner_id = int(settings.get_config("owner_id") or 0)
        self.database = database
        self.logger = logger

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
                if command["owner"] and event.from_id != self.owner_id:
                    print(f"Attempted owner command ({event.raw_text}) from ID {event.from_id}")
                    return

                event.args = pattern_match.groups()[-1]

                self.logger.info(f"Handling command '{command['pattern']}'")
                await command["function"](event)
