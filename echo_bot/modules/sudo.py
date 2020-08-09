from echo_bot import ldr


@ldr.add("stats", owner=True)
async def stats(event):
    await event.reply(ldr.database.get_stats())

@ldr.add("dump", owner=True)
async def dump(event):
    await event.reply(file=ldr.database.get_dump())

@ldr.add("unecho", owner=True)
async def unecho(event):
    unecho_text = await ldr.get_text(event)
    await event.reply(ldr.database.remove_echo(unecho_text))
