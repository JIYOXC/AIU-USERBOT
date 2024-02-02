# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

"""
✘ Commands Available -

• {i}w <text or reply to text>
   It will write on a paper.

"""

import os

from htmlwebshot import WebShot
from PIL import Image, ImageDraw, ImageFont

from . import async_searcher, eod, get_string, text_set, ultroid_cmd


@ultroid_cmd(pattern="nulis( (.*)|$)")
async def writer(e):
    if e.reply_to:
        reply = await e.get_reply_message()
        text = reply.message
    elif e.pattern_match.group(1).strip():
        text = e.text.split(maxsplit=1)[1]
    else:
        return await eod(e, get_string("writer_1"))
    k = await e.eor(get_string("com_1"))
    img = Image.open("resources/extras/template.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resources/fonts/default.ttf
    ", size=36)
    x, y = 150, 140
    lines = text_set(text)
    line_height = font.getbbox("\n")[3]
    for line in lines:
        draw.text((x, y), line, fill=(5, 22, 55), font=font)
        y = y + line_height - 5
    file = "ult.jpg"
    img.save(file)
    await e.reply(file=file)
    os.remove(file)
    await k.delete()
