import asyncio
from platform import python_version as pyver

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver

from MukeshRobot import SUPPORT_CHAT, pbot,BOT_USERNAME, OWNER_ID

PHOTO = [
    "https://graph.org/file/b71602972827efe0a89e1.jpg",
    "https://graph.org/file/3258ab01415c6823a4c94.jpg",
    "https://graph.org/file/3db4eb5ff387b4ef9722f.jpg",
    "https://graph.org/file/0b0f6da3760f9c45e2ecf.jpg",
    "https://graph.org/file/77a310c89c7b9cd5ee2c7.jpg",
]

Mukesh = [
    [
        InlineKeyboardButton(text="𝐎𝐰𝐧𝐞𝐫", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="𝐆𝐫𝐨𝐮𝐩", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="☆ 𝐀𝐝𝐝 𝐌𝐞 𝐌𝐨𝐢 𝐋𝐮𝐯 ☆",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

lol = "https://te.legra.ph/file/b2022725f36c2145787d1.jpg"


@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("⚡")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ...")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ....")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ.....")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ.......")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ.....ᴡᴀɪᴛ")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ..ᴡᴀɪᴛ ᴋᴀʀᴏ")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ........sᴜɴᴏ")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ.ɪᴋ ʙᴀᴀᴛ ʙᴏʟᴜɴ?")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ..............𝗜")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ...........𝗟𝗢𝗩𝗘")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ.............𝗬𝗢𝗨")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ..............😇😍")
    await asyncio.sleep(0.9)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ.............😍💞🥀")
    await accha.delete()
    await asyncio.sleep(0.9)
    umm = await m.reply_sticker(
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ"
    )
    await umm.delete()
    await asyncio.sleep(0.8)
    await m.reply_photo(
        lol,
        caption=f"""**🌷ʜᴇʏ, ɪ ᴀᴍ 『 ༎ࠫ🫧⛧‌ٖٖٖٖٖٖٜٖٖٖٖмιѕѕ qυєєи⛧‌ٖٖٖٖٖٖٜٖٖٖٖᥫᩣ●───♫▷(f"t.me/{BOT_USERNAME}")』🎄**
   ╔═════ஜ۩۞۩ஜ════╗

   💕𝗠𝗔𝗗𝗘 𝗕𝗬 [ɪɴɴᴏᴄᴇɴᴛ](https://t.me/Itzz_me_innocentt)💕

   ╚═════ஜ۩۞۩ஜ════╝""",
        reply_markup=InlineKeyboardMarkup(Mukesh),
    )
__mod_name__ = "⛧‌ᴀʟɪᴠᴇ⛧‌"
__help__ = """

*ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs*:
» /alive*:* ᴛᴏ ᴄʜᴇᴀᴋ ❓  ɪ ᴀᴍ ᴀʟɪᴠᴇ ᴏʀ ɴᴏᴛ?

☆............𝙱𝚈 » [ɪɴɴᴏᴄᴇɴᴛ](https://t.me/Itzz_me_innocentt)............☆"""
