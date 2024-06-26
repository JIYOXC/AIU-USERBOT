# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by Koala @manusiarakitann
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import os

import heroku3
from requests import get
from telethon.errors import FloodWaitError
from pyUltroid.configs import BLACKLIST_GCAST
#from pyUltroid.dB.blacklist_db import BLACKLIST_DB
from pyUltroid.dB.base import KeyManager
#from . import get_help, HEROKU_API_KEY, HEROKU_APP_NAME
from . import HNDLR, LOGS, eor, get_string, udB, ultroid_bot, ultroid_cmd
KeyM = KeyManager("BROADCAST", cast=list)
from . import GCAST_BLACKLIST

GCAST_BLACKLIST = [
    -1001675396283,  # AyiinXdSupport
    -1001473548283,  # SharingUserbot
    -1001433238829,  # TedeSupport
    -1001476936696,  # AnosSupport
    -1001327032795,  # UltroidSupport
    -1001294181499,  # UserBotIndo
    -1001419516987,  # VeezSupportGroup
    -1001459812644,  # GeezSupportGroup
    -1001296934585,  # X-PROJECT BOT
    -1001481357570,  # UsergeOnTopic
    -1001459701099,  # CatUserbotSupport
    -1001109837870,  # TelegramBotIndonesia
    -1001752592753,  # Skyzusupport
    -1001788983303,  # KayzuSupport
    -1001380293847,  # NastySupport
    -1001267233272,  # PocongUserbot
    -1001500063792,  # Trident
    -1001687155877,  # CilikSupport
    -1001662510083,  # MutualanDestra
    -1001347414136,  # ArunaMutualan
    -1001726206158,  # Nandesupport
    -1001608701614,  # Uputtsupport
    -1001578091827,  # PrimeSupport
    -1001599474353,  # HimikoSupport
    -1001287188817,  # KazuSupportGrp
    -1001302879778,  # KarmanSupport
    -1001638078842,  # RuangDiskusi
    -1001692751821,  # Geez|RAM Support
    -1001812143750,  # KynanSupport
]

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
blchat = os.environ.get("BLACKLIST_GCAST") or ""


@ultroid_cmd(pattern="gcast")
async def gcast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await eod(event, get_string("com_1"))
    kk = await eor(event, get_string("ex_1"))
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            if chat not in GCAST_BLACKLIST and chat not in BLACKLIST_GCAST:
                try:
                    await event.client.send_message(chat, msg)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(get_string("bd_2").format(done, er)
    )


@ultroid_cmd(pattern="gucast")
async def gucast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await eod(event, get_string("bd_1"))
    kk = await eor(event, get_string("bd_3"))
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            if chat not in DEVS:
                try:
                    await event.client.send_message(chat, msg)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(get_string("bd_4").format(done, er)
    )


@ultroid_cmd(pattern="blchat")
async def sudo(event):
    blacklistgc = "True" if BLACKLIST_GCAST else "False"
    blc = blchat
    list = blc.replace(" ", "\n» ")
    if blacklistgc == "True":
        await eor(
            event, get_string("bd_1").format(list, cmd)
        )
    else:
        await eod(event, get_string("bd_2"))


@ultroid_cmd(pattern="addbl")
async def addbl(event):
    xxnx = await eor(event, get_string("bd_1"))
    var = "BLACKLIST_GCAST"
    gc = event.chat_id
        await eod(
            xxnx, get_string("bd_1").format("menambahkan")
        )
        return
    blgc = f"{BLACKLIST_GCAST} {gc}"
    blacklistgrup = (
        blgc.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await xxnx.edit(get_string("bd_2").format(gc)
    )


@ultroid_cmd(pattern="delbl")
async def _(event):
    xxx = await eor(event, get_string("bd_1"))
    gc = event.chat_id
        await eod(
            xxx, get_string("bd_1").format("menghapus")
        )
        return
    gett = str(gc)
    if gett in blchat:
        blacklistgrup = blchat.replace(gett, "")
        await xxx.edit(get_string("bd_1").format(gc)
        )
        var = "BLACKLIST_GCAST"
    else:
        await eod(xxx, get_string("bd_2"), time=45
        )


