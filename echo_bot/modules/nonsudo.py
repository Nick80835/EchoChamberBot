from echo_bot import ldr


@ldr.add("echo")
async def forced_echo(event):
    await event.reply(ldr.database.get_random_echo())
