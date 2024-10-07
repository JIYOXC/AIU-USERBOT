import re
import base64
import requests
from os import remove
from . import ultroid_cmd, LOGS, run_async

@run_async
def analyze_image(encoded_image, prompt, bid):
    url = 'https://bot-management-4tozrh7z2a-ue.a.run.app/chat/see'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Origin': 'https://app.paal.ai',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://app.paal.ai/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    data = {
        "base64_image": encoded_image,
        "prompt": prompt,
        "bid": bid  # Adding the 'bid' field here
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

@ultroid_cmd(pattern="see(image)?( (.*)|$)")
async def analyze_image_cmd(e):
    reply = await e.get_reply_message()
    
    if not reply or not reply.media:
        return await e.eor("Please reply to an image to analyze.")
    
    moi = await e.eor("Downloading image...")
    downloaded_media = await e.client.download_media(reply.media)
    
    if not downloaded_media:
        return await moi.edit("Failed to download media.")
    
    try:
        with open(downloaded_media, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as exc:
        LOGS.warning(exc, exc_info=True)
        await moi.edit(f"Error during file read/encode: {exc}")
        return
    finally:
        remove(downloaded_media)
    
    prompt = e.pattern_match.group(3) or "Provide a description of the person in the image."
    bid = "some_bid_value"  # Replace with the actual 'bid' value as needed
    
    try:
        response = await analyze_image(encoded_image, prompt, bid)
        if response:
            formatted_response = re.sub(r'\\(.*?)\\', r'**\1**', response.replace("\\n", "\n"))
            response_str = str(formatted_response)
        else:
            response_str = str(response)
        
        if len(response_str) > 4096:
            file_name = "response.txt"
            with open(file_name, "w") as file:
                file.write(response_str)
            
            await e.client.send_file(e.chat_id, file_name, caption="Response was too long, so here it is in a file.")
            remove(file_name)
        else:
            await moi.edit(f"{response_str}")
    except Exception as exc:
        LOGS.warning(exc, exc_info=True)
        await moi.edit(f"Error: {exc}")
