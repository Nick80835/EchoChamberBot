from logging import Logger

from echo_bot.database import Database
from echo_bot.settings import Settings
from telethon import TelegramClient, events


class EchoHandler:
    database = Database()

    def __init__(self, settings: Settings, logger: Logger):
        self.owner_id = int(settings.get_config("owner_id") or 0)
        self.settings = settings
        self.logger = logger

    def start_handler(self, client: TelegramClient):
        client.add_event_handler(self.handle_incoming, events.NewMessage(incoming=True))

    async def handle_incoming(self, event):
        if not event.is_private or not event.raw_text or (event.raw_text.startswith("/") and event.from_id != self.owner_id):
            return

        if event.raw_text.startswith("/"):
            await self.handle_command(event)
            return

        self.logger.info("Handling an echo!")
        await event.client.send_message(event.from_id, self.database.get_random_echo())
        self.database.add_to_echoes(event.raw_text)

    async def handle_command(self, event):
        if event.raw_text == "/stats":
            await event.client.send_message(event.from_id, self.database.get_stats())
