import sys
from logging import INFO, basicConfig, getLogger

from echo_bot.database import Database
from echo_bot.echo_handler import EchoHandler
from echo_bot.loader import Loader
from echo_bot.settings import Settings
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.network.connection.tcpabridged import \
    ConnectionTcpAbridged as CTA

from .command_handler import CommandHandler


class EchoChamberBot:
    settings = Settings()
    database = Database()

    def __init__(self):
        basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO)
        self.logger = getLogger(__name__)
        self.command_handler = CommandHandler(self.database, self.logger, self.settings)
        self.echo_handler = EchoHandler(self.settings, self.logger, self.database, self.command_handler)
        self._start_client()
        self.loader = Loader(self.client, self.logger, self.settings, self.database, self.command_handler)

    def run_until_done(self):
        self.loader.load_all_modules()
        self.logger.info("Client successfully started.")
        self.echo_handler.start_handler(self.client)
        self.logger.info("Echo handler successfully started.")
        self.client.run_until_disconnected()

    def _check_config(self):
        api_key = self.settings.get_config("api_key")
        api_hash = self.settings.get_config("api_hash")
        bot_token = self.settings.get_config("bot_token")

        while not api_key:
            api_key = input("Enter your API key: ")

        self.settings.set_config("api_key", api_key)

        while not api_hash:
            api_hash = input("Enter your API hash: ")

        self.settings.set_config("api_hash", api_hash)

        while not bot_token:
            bot_token = input("Enter your bot token: ")

        self.settings.set_config("bot_token", bot_token)

        return api_key, api_hash, bot_token

    def _start_client(self):
        api_key, api_hash, bot_token = self._check_config()
        self.client = TelegramClient("echo_bot", api_key, api_hash, connection=CTA)

        try:
            self.client.start(bot_token=bot_token)
        except PhoneNumberInvalidError:
            print("The bot token provided is invalid, exiting.")
            sys.exit(2)

    async def stop_client(self):
        await self.client.disconnect()


echo_bot = EchoChamberBot()
ldr = echo_bot.loader

try:
    echo_bot.run_until_done()
except:
    echo_bot.client.loop.run_until_complete(echo_bot.stop_client())
