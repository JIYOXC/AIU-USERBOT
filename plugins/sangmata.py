# written by @lazy_raion



"""
Sangmata Beta!

CMD: {i}sgb <reply/user_id>
"""

from asyncio import sleep, TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import get_string, LOGS, ultroid_cmd


CHAT = "SangMata_beta_bot"

@ultroid_cmd(
    pattern="sgb( (.*)|$)",
)
async def sangmata_beta(e):
    args = e.pattern_match.group(2)
    reply = await e.get_reply_message()
    if args:
        try:
            user_id = await e.client.parse_id(args)
        except ValueError:
            user_id = args
    elif reply:
        user_id = reply.sender_id
    else:
        return await e.eor("Use this command with reply or give Username/id...")

    lol = await e.eor(get_string("com_1"))
    try:
        async with e.client.conversation(CHAT, total_timeout=15) as conv:
            msg = await conv.send_message(f"@SangMata_beta_bot allhistory {user_id}")
            response = await conv.get_response()
            if response and "no data available" in response.text.lower():
                await lol.edit("okbie, No records found for this user")
            elif str(user_id) in response.message:
                await lol.edit(response.text)
    except YouBlockedUserError:
        return await lol.edit(f"Please unblock @{CHAT} and try again.")
    except TimeoutError:
        await lol.edit("Bot didn't respond in time.")
    except Exception as ex:
        LOGS.exception(ex)
        await lol.edit(f"Error: {ex}")
    finally:
        await sleep(2)
        await e.client.send_read_acknowledge(CHAT)