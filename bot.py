import os
import string
import asyncio
import requests
import math
import time
from datetime import timedelta
from pyrogram import Client, filters


TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

APP_ID = int(os.environ.get("APP_ID", ""))

API_HASH = os.environ.get("API_HASH", "")


app = Client("tgid", bot_token=TG_BOT_TOKEN, api_hash=API_HASH, api_id=APP_ID)


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def convert(n):
   return str(timedelta(seconds = n))


@app.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"Hello 👋\n\nSend me Any MDisk links to convert it into Direct Download Link.Request any movies series here <b> @Blackest_harbour </b>", reply_to_message_id=message.message_id)


@app.on_message(filters.private & filters.text)
async def link_extract(bot, message):
    urls = message.text
    
    if not message.text.startswith("https://mdisk.me"):
        await message.reply_text(
            f"**INVALID LINK**",
            reply_to_message_id=message.message_id
        )
        return
    a = await bot.send_message(
            chat_id=message.chat.id,
            text=f"Processing…",
            reply_to_message_id=message.message_id
        )
    inp = urls #input('Enter the Link: ')
    fxl = inp.split("/")
    cid = fxl[-1]
    URL=f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}'
    header = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://mdisk.me/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }
    resp = requests.get(url=URL, headers=header).json()
    fn = resp['filename']
    dn = resp['display_name']
    dr = resp['duration']
    sz = resp['size']
    ht = resp['height']
    wt = resp['width']
    download = resp['download']
    
    await a.edit_text("**Title:** {}\n**Size:** {}\n**Duration:** {}\n**Resolution:** {}*{}\n**Uploader:** {}\n\n**Download Now:** {}".format(fn, humanbytes(sz), convert(dr), wt, ht, dn, download), disable_web_page_preview=True)
    


app.run()
