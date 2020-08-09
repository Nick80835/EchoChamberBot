# SPDX-License-Identifier: GPL-2.0-or-later

import glob
from importlib import import_module
from os.path import basename, dirname, isfile


class Loader():
    all_modules = []

    def __init__(self, client, logger, settings, database, command_handler):
        self.client = client
        self.logger = logger
        self.settings = settings
        self.database = database
        self.command_handler = command_handler

    def load_all_modules(self):
        self._find_all_modules()

        for module_name in self.all_modules:
            try:
                import_module("echo_bot.modules." + module_name)
            except Exception as exception:
                self.logger.error(f"Error while loading {module_name}: {exception}")

    def add(self, pattern=None, **args):
        pattern = args.get("pattern", pattern)

        def decorator(func):
            self.command_handler.commands.append({
                "pattern": pattern,
                "function": func,
                "owner": args.get('owner', False)
            })

            return func

        return decorator

    async def get_text(self, event, default=None):
        if event.args:
            return event.args

        if event.is_reply:
            reply = await event.get_reply_message()
            return reply.raw_text

        return default

    def _find_all_modules(self):
        module_paths = glob.glob(dirname(__file__) + "/modules/*.py")

        self.all_modules = sorted([
            basename(f)[:-3] for f in module_paths
            if isfile(f) and f.endswith(".py")
        ])
