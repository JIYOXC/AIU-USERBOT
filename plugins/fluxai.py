#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2024 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import io
import time

import requests
from PIL import Image
#from pyrogram import *
from pyrogram import Client, filters
#from pyrogram.types import *

from . import LOGS, asst, ultroid_bot, ultroid_cmd
from pyUltroid.fns.scripts import progress
#from config import CMD_HANDLER, DOMAIN_DEV_API


async def schellwithflux(args, is_working_dev=False):
    if is_working_dev:
        API_URL = f"https://akeno.randydev.my.id/api/v1/akeno/fluxai"
    else:
        API_URL = "https://randydev-ryuzaki-api.hf.space/api/v1/akeno/fluxai"
    payload = {
        "user_id": 1191668125,  # Please don't edit here
        "api_key": "6398769dabd9fe0e49bedce0354b40a9b1a69d9594dc9d48c1d8a2a071c51e89",
        "args": args
    }
    response = requests.post(API_URL, json=payload)
    if response.status_code != 200:
        LOGS.error(f"Error status {response.status_code}")
        return None
    return response.content

@ultroid_cmd(
    pattern="fluxai( (.*)|$)",
)
async def imgfluxai_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Please provide a question for Flux.")
    try:
        image_bytes = await schellwithflux(question)
        if image_bytes is None:
            return await message.reply_text("Failed to generate an image.")
        pro = await message.reply_text("Generating image, please wait...")
        with open("flux_gen.jpg", "wb") as f:
            f.write(image_bytes)
        ok = await pro.edit_text("Uploading image...")
        await message.reply_photo("flux_gen.jpg", progress=progress, progress_args=(ok, time.time(), "Uploading image..."))
        await ok.delete()
        if os.path.exists("flux_gen.jpg"):
            os.remove("flux_gen.jpg")
    except Exception as e:
        LOGS.error(str(e))
        await message.edit_text(str(e))
      
