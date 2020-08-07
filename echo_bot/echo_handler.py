from logging import Logger

from echo_bot.command_handler import CommandHandler
from echo_bot.database import Database
from echo_bot.settings import Settings
from telethon import TelegramClient, events


class EchoHandler:
    database = Database()

    def __init__(self, settings: Settings, logger: Logger):
        self.owner_id = int(settings.get_config("owner_id") or 0)
        self.command_handler = CommandHandler(self.database, logger)
        self.settings = settings
        self.logger = logger

    def start_handler(self, client: TelegramClient):
        client.add_event_handler(self.handle_incoming, events.NewMessage(incoming=True))

    async def handle_incoming(self, event):
        if self.is_junk(event):
            self.logger.info(f"Discarding junk: {event.raw_text}")
            return

        try:
            if event.raw_text.startswith("/"):
                if event.raw_text == "/echo":
                    await event.reply(self.database.get_random_echo())
                    return

                if event.from_id == self.owner_id:
                    self.logger.info(f"Passing to command handler: {event.raw_text}")
                    await self.command_handler.handle_command(event)
                    return

                return

            if not event.is_private:
                self.database.add_to_echoes(event.raw_text)
                return

            self.logger.info("Handling an echo!")
            await event.client.send_message(event.from_id, self.database.get_random_echo())
            self.database.add_to_echoes(event.raw_text)
        except Exception as exception:
            await event.client.send_message(self.owner_id, f"I encountered an error: {exception}")
            raise exception

    def is_junk(self, event) -> bool:
        if not event.raw_text:
            return True

        if event.from_id != self.owner_id and event.raw_text.lower().startswith(("!", "g.", "r.", "noi")):
            return True

        if event.from_id == self.owner_id and event.raw_text.lower().startswith(("!", "g.", "r.", "noi")):
            return True

        return False
