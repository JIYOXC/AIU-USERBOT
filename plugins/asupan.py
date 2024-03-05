from telethon.tl.types import InputMessagesFilterVideo

@ultroid_cmd(pattern="asupan")
async def _(e):
    xx = await e.eor( "Tunggu Sebentar...")
    try:
        asupann = [
                          asupan
                          async for asupan in e.client.iter_messages(
            "@tedeasupancache", filter=InputMessagesFilterVideo
            )
        ]
        await e.client.send_file(
            e.chat_id, reply_to=e.reply_to_msg_id
            )
        await xx.delete()
    except Exception as e:
        await xx.edit(f"Error {e}\nTidak bisa menemukan video asupan.")

