from random import choice

from telethon.events import NewMessage
from telethon.tl.types import ReactionEmoji

from . import ultroid_bot, ultroid_cmd


EMO = ('🥱', '🤪', '🙉', '😍', '🦄', '🐳', '😘', '💘', '😈', '❤️‍🔥', '🌭', '❤️', '🤔', '🎄', '🥴', '💩', '😁', '👾', '👨‍💻', '🕊', '😐', '👌', '👍', '🔥', '🙈', '🤬', '💋', '😴', '🤷', '🆒', '🤓', '🍌', '😡', '🤡', '👀', '💔', '🤗', '☃️', '🙊', '😭', '🤮', '✍️', '🎃', '😇', '👻', '🏆', '🤝', '💯', '😢', '😱', '🤯', '🤨', '🌚', '😨', '⚡️', '🎉', '🫡', '🤩', '🥰', '🍾', '👏', '🙏', '🎅', '😎', '💊', '👎', '🤣', '🗿', '💅', '🍓', '🖕', '🤷‍♂️', '🤷', '🤷‍♀️')


async def autoreact(e):
    try:
        emoji = choice(EMO)
        await e.react([ReactionEmoji(emoji)])
    except Exception:
        pass


def autoreact_status():
    for func, _ in ultroid_bot.list_event_handlers():
        if func == autoreact:
            return True


@ultroid_cmd(pattern="autoreact( (.*)|$)")
async def self_react(e):
    args = e.pattern_match.group(2)
    eris = await e.eor("...")
    if args == "on":
        if autoreact_status():
            return await eris.edit("AutoReact is Already Enabled..")
        ultroid_bot.add_event_handler(
            autoreact,
            NewMessage(
                outgoing=True,
                func=lambda e: not (e.fwd_from or e.via_bot),
            )
        )
        await eris.edit("AutoReact Enabled!")
    elif args == "off":
        if not autoreact_status():
            return await eris.edit("AutoReact is Already Disabled..")
        ultroid_bot.remove_event_handler(autoreact)
        await eris.edit("AutoReact Disabled!")
    else:
        await eris.edit("Usage: .autoreact on/off")