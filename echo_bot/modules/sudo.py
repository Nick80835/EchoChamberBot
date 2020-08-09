from io import BytesIO

from echo_bot import ldr


@ldr.add("stats", owner=True)
async def stats(event):
    await event.reply(ldr.database.get_stats())

@ldr.add("dump", owner=True)
async def dump(event):
    await event.reply(file=ldr.database.get_dump())

@ldr.add("overwrite", owner=True)
async def overwrite(event):
    overwrite_io = BytesIO()

    if event.is_reply:
        reply = await event.get_reply_message()

        if reply.file and reply.file.name.endswith(".txt"):
            await event.client.download_media(reply.media.document, overwrite_io)
            print(overwrite_io.read())
            ldr.database.overwrite(overwrite_io)
            await event.reply("Successfully overwrote database!")
            return
    elif event.file and event.file.name.endswith(".txt"):
        await event.client.download_media(event.media.document, overwrite_io)
        ldr.database.overwrite(overwrite_io)
        await event.reply("Successfully overwrote database!")
        return

    await event.reply("I need a file to overwrite my database with!")

@ldr.add("unecho", owner=True)
async def unecho(event):
    unecho_text = await ldr.get_text(event)
    await event.reply(ldr.database.remove_echo(unecho_text))
