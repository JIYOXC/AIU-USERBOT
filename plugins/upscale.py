import os
import base64
import requests
from . import LOGS, con

try:
    import cv2
except ImportError:
    LOGS.error(f"{file}: OpenCv not Installed.")

import numpy as np

try:
    from PIL import Image
except ImportError:
    Image = None
    LOGS.info(f"{file}: PIL  not Installed.")
from telegraph import upload_file as upf
from telethon.errors.rpcerrorlist import (
    ChatSendMediaForbiddenError,
    MessageDeleteForbiddenError,
)

from . import (
    Redis,
    async_searcher,
    download_file,
    get_string,
    requests,
    udB,
    ultroid_cmd,
)


@ultroid_cmd(pattern="upscale$")
async def enhance_image(event):
    reply_message = await event.get_reply_message()
    if not (reply_message and (reply_message.photo or reply_message.sticker)):
        return await event.eor("Reply to a photo")

    msg = await event.eor("Upscaling image...")
    image = await reply_message.download_media()

    # Read image file into binary data
    with open(image, 'rb') as f:
        image_data = f.read()

    # Encode binary image data to base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')

    # Construct the JSON payload
    payload = {
        "resize_mode": 0,
        "show_extras_results": True,
        "gfpgan_visibility": 0,
        "codeformer_visibility": 0,
        "codeformer_weight": 1,
        "upscaling_resize": 2,
        "upscaler_1": "4xUltrasharpV10",
        "upscaler_2": "R-ESRGAN 4x+",
        "upscale_first": False,
        "image": encoded_image
    }

    # Set up headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic cGljYXRvYXBpOko3XnMxazYqaTJA"
    }

    # Send the POST request
    response = requests.post('http://110.93.223.194:5670/sdapi/v1/extra-single-image', json=payload, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Extract enhanced image data from response
        response_data = response.json()
        enhanced_image_base64 = response_data.get('image')

        # Decode base64 image data
        enhanced_image_binary = base64.b64decode(enhanced_image_base64)

        # Save the enhanced image to a file
        enhanced_image_path = 'upscale_image.jpg'
        with open(enhanced_image_path, 'wb') as img_file:
            img_file.write(enhanced_image_binary)

        # Upload enhanced image both as a file and as a photo
        await event.client.send_file(event.chat_id, enhanced_image_path, reply_to=reply_message)
        await event.client.send_file(event.chat_id, enhanced_image_path, force_document=True, reply_to=reply_message)

        # Clean up files
        os.remove(enhanced_image_path)
        os.remove(image)

        await msg.delete()
    else:
        await msg.edit("Failed to upscale image.")
