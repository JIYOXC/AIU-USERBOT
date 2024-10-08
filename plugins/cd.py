# < Source - t.me/testingpluginnn >
# < https://github.com/TeamUltroid/Ultroid >

"""
✘ **Send any Installed Plugin to the Chat!**

>> Use : `{i}cd <plugin_name>`
"""

import os

from . import *
async def get_paste(data: str, extension: str = "txt"):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    json = {"content": data, "extension": extension}
    key = await async_searcher(
        url="https://spaceb.in/api/",
        json=json,
        ssl=ssl_context,
        post=True,
        re_json=True,
    )
    try:
        return True, key["payload"]["id"]
    except KeyError:
        if "the length must be between 2 and 400000." in key["error"]:
            return await get_paste(data[-400000:], extension=extension)
        return False, key["error"]
    except Exception as e:
        LOGS.info(e)
        return None, str(e)


def send(fn):
    lst = ["plugins", "addons"]
    if not fn.endswith(".py"):
        fn += ".py"
    for i in lst:
        path = os.path.join(i, fn)
        if os.path.exists(path):
            return path
    else:
        return


def alt_send(fn):
    import re
    for k, v in LIST.items():
        for fx in v:
            if re.findall(fn, fx):
                return send(k)
    else:
        return


async def pastee(path):
    with open(path, "r") as f:
        data = f.read()
    err, linky = await get_paste(data)
    if err:
        return f"<b>>> <a href='https://spaceb.in/{linky}'>Pasted Here!</a></b> \n"
    else:
        LOGS.error(linky)
        return ""


@ultroid_cmd(pattern="cd ?(.*)")
async def semd_plugin(ult):
    repo = "https://github.com/JIYOXC/AIU-USERBOT"
    args = ult.pattern_match.group(1)
    if not args:
        return await ult.eod("`Give a plugin name too`")

    eris = await ult.eor("`...`")
    path = send(args)
    if not path:
        path = alt_send(args)
    if not path:
        return await eris.edit(f"No plugins were found for: `{args}`")

    paste = await pastee(path)
    caption = f"<b>>> </b><code>{path}</code> \n{paste} \n" \
        f"© <a href='{repo}'>AIU-USERBOT</a>"
    try:
        await ult.client.send_file(
            ult.chat_id, path,
            caption=caption, parse_mode="html",
            silent=True, reply_to=ult.reply_to_msg_id,
        )
        await eris.delete()
    except Exception as fx:
        return await eris.edit(str(fx))
