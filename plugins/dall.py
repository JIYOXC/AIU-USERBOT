import aiohttp
import json
import os
from os import system, remove

from . import ultroid_cmd, check_filename, fast_download

async def paal_image(prompt):
    url = "https://bot-management-4tozrh7z2a-ue.a.run.app/chat/image"
    headers = {
        "content-type": "application/json",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "accept": "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?1",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "sec-ch-ua-platform": '"Android"',
        "origin": "https://app.paal.ai",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://app.paal.ai/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    payload = {"prompt": prompt, "bid": "edwo6pg1", "history": []}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
            data = await response.json()
            if "url" not in data:
                raise Exception("Image URL not found in the response.")
            image_url = data["url"]

        async with session.get(image_url) as image_response:
            if image_response.status != 200:
                raise Exception(f"Failed to retrieve image from URL: {image_response.status}")
            image_content = await image_response.read()

    image_path = check_filename("generated_image.png")
    with open(image_path, "wb") as image_file:
        image_file.write(image_content)

    return image_path

@ultroid_cmd(pattern="dall( (.*)|$)")
async def generate_image(event):
    args = event.pattern_match.group(2)

    if not args and event.is_reply:
        replied_message = await event.get_reply_message()
        args = replied_message.text.strip()

    if not args:
        return await event.eor("Please provide a prompt for generating the image.")

    moi = await event.eor("Generating image...")
    try:
        # Await the image creation
        image_path = await paal_image(args.strip())
        if len(f"Generated Image\nPrompt: {args}") <= 1024:
            await event.client.send_file(
                event.chat_id,
                image_path,
                caption=f"Generated Image\nPrompt: {args}",
                reply_to=event.reply_to_msg_id,
            )
        else:
            await event.client.send_file(
                event.chat_id,
                image_path,
                reply_to=event.reply_to_msg_id,
            )
        remove(image_path)
        await moi.delete()
    except Exception as exc:
        await moi.edit(f"Error: {exc}")
