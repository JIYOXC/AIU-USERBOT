import os
from collections import deque
from io import BytesIO
import openai
import requests

from . import (
    ultroid_cmd,
    async_searcher,
    check_filename,
    udB,
    LOGS,
    download_file,
    run_async,
)


GPT_CHAT_HISTORY = deque(maxlen=30)

TELEGRAM_CHAR_LIMIT = 4096  # Telegram's message character limit

@ultroid_cmd(
    pattern=r"ask( ([\s\S]*)|$)",
)
async def openai_chat_gpt(e):
    api_key = udB.get_key("OPENAI_API")
    if not api_key:
        return await e.eor("`OPENAI_API` key missing..", time=10)

    query = e.pattern_match.group(2)
    if not query:
        reply = await e.get_reply_message()
        if reply and reply.text:
            query = reply.message
    if not query:
        return await e.eor("`Gimme a Question to ask from GPT-4o..`", time=5)

    if query == "-c":
        GPT_CHAT_HISTORY.clear()
        return await e.eor("__Cleared GPT-4o Chat History!__", time=6)

    eris = await e.eor(f"__Generating answer for:__\n`{query[:128]} ...`")
    GPT_CHAT_HISTORY.append({'role': 'user', 'content': query})

    try:
        data = {
            "model": "Gemini 1.5 Flash",
            "messages": list(GPT_CHAT_HISTORY),
        }
        request = await async_searcher(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json=data,
            re_json=True,
            post=True,
        )
        response = request['choices'][0]['message']['content']
        GPT_CHAT_HISTORY.append({'role': 'assistant', 'content': response})
    except Exception as exc:
        LOGS.warning(exc, exc_info=True)
        GPT_CHAT_HISTORY.pop()
        return await eris.edit(
            f"**Error while requesting data from OpenAI:** \n> `{exc}`"
        )

    LOGS.debug(f'Token Used on ({query}) > {request["usage"]["completion_tokens"]}')
    
    # Truncate query to 400 characters
    truncated_query = query[:400]

    # Prepare the full message
    full_message = f"**Query:**\n~ __{truncated_query}__\n\n**GPT-4o:**\n~ {response}"
    
    if len(full_message) <= TELEGRAM_CHAR_LIMIT:
        # If it fits within the limit, send as a message
        return await eris.edit(full_message)
    else:
        # If it exceeds the limit, send as a file
        with BytesIO(full_message.encode()) as file:
            file.name = "gpt-4o-output.txt"
            await eris.respond(
                "__The query and response were too long, so they have been sent as a file.__",
                file=file,
                reply_to=e.reply_to_msg_id or e.id,
            )
        await eris.try_delete()
      
