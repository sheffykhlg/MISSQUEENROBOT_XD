import glob
import io
import os
import random

import requests
from PIL import Image, ImageDraw, ImageFont

from MukeshRobot import BOT_NAME, BOT_USERNAME, OWNER_ID, telethn
from MukeshRobot.events import register

LOGO_LINKS = [
    "https://graph.org/file/7afcc8709949b975abf4e.jpg"
"https://graph.org/file/4518ad51ff32569c51829.jpg"
"https://graph.org/file/82d99b4eed5b239991bfa.jpg"
"https://graph.org/file/7bcffe78452629ff11f02.jpg"
"https://graph.org/file/e86ade56540a0e7581a34.jpg"
"https://graph.org/file/a39ecb8d01f9beb60c3b4.jpg"
"https://graph.org/file/1ed99c14103244fa2da7d.jpg"
"https://graph.org/file/9ce0a96efbe6a0b42908e.jpg"
"https://graph.org/file/761c955fe13996f2aa4ae.jpg"
"https://graph.org/file/2875034d0915cf0f05994.jpg"
"https://graph.org/file/c47a08eff6e7b93d9d98c.jpg"
"https://graph.org/file/c66ede0e1ed6cea5a7dcc.jpg"
"https://graph.org/file/93213c27fbb478c83e5ef.jpg"
"https://graph.org/file/327a0789b6902ee4a3db5.jpg"
"https://graph.org/file/fc4a624cc38ccd2d2499b.jpg"
"https://graph.org/file/2ea286802e0f51182f5f5.jpg"
"https://graph.org/file/b873d2766c81dd8686608.jpg"
"https://graph.org/file/439e9c70c642a64bd9554.jpg"
"https://graph.org/file/5814af9167bf18a71ffd6.jpg"
"https://graph.org/file/3255def0594c49dac415d.jpg"
"https://graph.org/file/ce5b7096c3e789f1d4caa.jpg"
"https://graph.org/file/9dc9062a765c2d2027e2d.jpg"
"https://graph.org/file/282e87f3098cbf555b5ea.jpg"
"https://graph.org/file/3ef669c3f6bfb8bea4088.jpg"
"https://graph.org/file/6eaba405002ddedbd1062.jpg"
"https://graph.org/file/1fa068a1ff04b6931ffe7.jpg"
"https://graph.org/file/c042ca2264feb50e6ee1f.jpg"
"https://graph.org/file/69547984cc7557d99d5be.jpg"
"https://graph.org/file/ae90dfa2490084594b24d.jpg"
"https://graph.org/file/aba1b8fbb2e3e18fbfb73.jpg"
"https://graph.org/file/352e1deb863f23b13972e.jpg"
"https://graph.org/file/aee43fe0943025203a443.jpg"
"https://graph.org/file/f9981dd9a9aa181cfc049.jpg"
"https://graph.org/file/238d68f816979eb158fbe.jpg"
"https://graph.org/file/010f6d300464b0091e1c8.jpg"
"https://graph.org/file/f66d30a366c31b6f4c1c9.jpg"
"https://graph.org/file/56daf576cd66e2fe762f1.jpg"
"https://graph.org/file/e5aa73d641915727e5485.jpg"
"https://graph.org/file/85a85c7a5766e494d43e4.jpg"
"https://graph.org/file/d9fa10af97b761ef41c62.jpg"
"https://graph.org/file/b76a85a2b81e18243994e.jpg"
"https://graph.org/file/2e764e2fb37e2eecc7b00.jpg"
"https://graph.org/file/e535e3c0101d645a25001.jpg"
"https://graph.org/file/300417dec7ae53ac95bcf.jpg"
"https://graph.org/file/30aeb1bcdc189bf1e97dd.jpg"
"https://graph.org/file/23f906a67cf9c6a0ff59c.jpg"
"https://graph.org/file/4f097fbfb6adc98c0f703.jpg"
"https://graph.org/file/767b59ee3f97070877309.jpg"
"https://graph.org/file/c970ad40d45b44c5b3a6b.jpg"
"https://graph.org/file/debf60de6eb0ff6344d2e.jpg"
"https://graph.org/file/b689659e446c4a8266686.jpg"
"https://graph.org/file/8c0bc110573193cad9e90.jpg"
"https://graph.org/file/61bd51e64c3be2ac02fd3.jpg"
"https://graph.org/file/e94c00587ac9b32368c7c.jpg"
"https://graph.org/file/6d579487a96bc99a3a4cc.jpg"
"https://graph.org/file/7536ce33b9aa442fc1647.jpg"
"https://graph.org/file/197d40d373cb353f794f1.jpg"
"https://graph.org/file/3db3ba54f6f313c6cf20a.jpg"
"https://graph.org/file/821f065b34af3cf7447b4.jpg"
"https://graph.org/file/8f0918cf9a277d3ea6cef.jpg"
"https://graph.org/file/360676a2c160029e03e46.jpg"
"https://graph.org/file/8427f9376e7caf2ddd5c0.jpg"
"https://graph.org/file/9ba04d3afc95ac650d24b.jpg"
"https://graph.org/file/6a62e5f88b2ffecf5a656.jpg"
"https://graph.org/file/7efaf77922459c958fcb4.jpg"
"https://graph.org/file/9a41171c9e4bda10325b5.jpg"
"https://graph.org/file/d36b5fe2777ef7aec09d1.jpg"
"https://graph.org/file/370b80fd7d886691dd98c.jpg"
"https://graph.org/file/77a310c89c7b9cd5ee2c7.jpg"
"https://graph.org/file/3f1f8adf4982f1261e2dc.jpg"
"https://graph.org/file/e5acb1597514ee308fca5.jpg"
"https://graph.org/file/f4d968488e0431e250620.jpg"
"https://graph.org/file/eef025fbd32e267bc2284.jpg"
"https://graph.org/file/0b0f6da3760f9c45e2ecf.jpg"
"https://graph.org/file/3258ab01415c6823a4c94.jpg"
"https://graph.org/file/b435ed53cde5b4cf36f8d.jpg"
"https://graph.org/file/3db4eb5ff387b4ef9722f.jpg"
"https://graph.org/file/bcc8df6e778955f4b0c1d.jpg"
]


@register(pattern="^/logo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id != OWNER_ID and not quew:
        await event.reply(
            "ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʀᴇᴀᴛᴇ ʟᴏɢᴏ ʙᴀʙʏ​ !\nExample : `/logo <VIP BOY>`"
        )
        return
    pesan = await event.reply("**ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏɢᴏ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ​...**")
    try:
        text = event.pattern_match.group(1)
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = glob.glob("./MukeshRobot/resources/fonts/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "mukesh.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f"ʟᴏɢᴏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME})",
        )
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)
    except Exception:
        text = event.pattern_match.group(1)
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = glob.glob("./MukeshRobot/resources/fonts/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "mukesh.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f"ʟᴏɢᴏ ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ [{BOT_NAME}](https://t.me/{BOT_USERNAME})",
        )
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)


__mod_name__ = "⛧‌ʟᴏɢᴏ⛧‌"

__help__ = """
I can create some beautiful and attractive logo for your profile pics.

❍ /logo (Text) *:* Create a logo of your given text with random view.
"""
