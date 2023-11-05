import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import MukeshRobot.modules.sql.users_sql as sql
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
PM_START_TEX = """
🍷𝐖𝐞𝐥𝐜𝐨𝐦𝐞 `{}`, 🍷 
"""


PM_START_TEXT = """ 

👀𝐇𝐞𝐲 {} , [🖤]({})

╔══❰🌺𝐖𝐄𝐋𝐂𝐎𝐌𝐄🌺❱═══❍⊱❁۪۪
║
║┣⪼ {} 
║
╚═════════════════❍⊱❁۪۪
      ╔═════ஜ۩۞۩ஜ════╗

        💞 ᴍᴀᴅᴇ ʙʏ ɪɴɴᴏᴄᴇɴᴛ 💞
    
      ╚═════ஜ۩۞۩ஜ════╝

ɪ ᴀᴍ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴅ sᴜᴘᴇʀғᴀsᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴀɴᴅ ᴠᴄ ᴘʟᴀʏᴇʀ ᴡɪᴛʜ 24x7 ᴀᴄᴛɪᴠᴇ » ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘs ᴀɴᴅ ᴄʜᴀɴɴᴇʟ

ғᴇᴇʟ ʟᴀɢ ғʀᴇᴇ ᴛᴏ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴇɴᴊᴏʏ sᴜᴘᴇʀ ʜɪɢʜ ǫᴜᴀʟɪᴛʏ ᴍᴀɴᴀɢɪɴɢ-ɢʀᴏᴜᴘ &  ᴘʟᴀʏ ᴀᴜᴅɪᴏ ᴀɴᴅ ᴠɪᴅᴇᴏ

☆............𝙱𝚈 » [ɪɴɴᴏᴄᴇɴᴛ](https://t.me/Itzz_me_innocentt)............☆
"""

buttons = [
    [
        InlineKeyboardButton(
            text="✭ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ✭",
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="✭𝙷𝙴𝙻𝙿 ♡︎ 𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂✭", callback_data="help_back"),
        InlineKeyboardButton(text="⎯꯭‌✭𝆺꯭𝅥𝙼𝚄𝚂𝙸𝙲✭", callback_data="Music_"),
    ],
    [
        InlineKeyboardButton(text="⎯꯭‌✭𝆺꯭𝅥𝚂𝚄𝙿𝙿𝙾𝚁𝚃✭", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(text="⎯꯭‌✭𝆺꯭𝅥𝚄𝙿𝙳𝙰𝚃𝙴✭", url=f"https://t.me/khamoshiya01"),
    ],
    [
        InlineKeyboardButton(text="⎯꯭‌✭𝆺꯭𝅥ᴿᴱᴾᴼ .𓈀✔", callback_data="mukesh_"),
    ],
]

HELP_STRINGS = f"""
» {BOT_NAME}  ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄs ᴄᴏᴍᴍᴀɴᴅ"""

DONATE_STRING = """ʜᴇʏ ʙᴀʙʏ,
  ʜᴀᴩᴩʏ ᴛᴏ ʜᴇᴀʀ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ.

ʏᴏᴜ ᴄᴀɴ ᴅɪʀᴇᴄᴛʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ [ᴅᴇᴠᴇʟᴏᴩᴇʀ](f"tg://user?id={OWNER_ID}") ғᴏʀ ᴅᴏɴᴀᴛɪɴɢ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴠɪsɪᴛ ᴍʏ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](f"https://t.me/{SUPPORT_CHAT}") ᴀɴᴅ ᴀsᴋ ᴛʜᴇʀᴇ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("MukeshRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    update.effective_message.reply_text(
        "Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN
    )
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
                "CAACAgUAAxkBAAI33mLYLNLilbRI-sKAAob0P7koTEJNAAIOBAACl42QVKnra4sdzC_uKQQ")
            x.delete()
            usr = update.effective_user
            lol = update.effective_message.reply_text(
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN
            )
            time.sleep(0.4)
            lol.edit_text("𝗦𝗧𝗔𝗥𝗧𝗜𝗡𝗚.")
            time.sleep(0.4)
            lol.edit_text("𝗦𝗧𝗔𝗥𝗧𝗜𝗡𝗚 𝗕𝗢𝗧......😉")
            time.sleep(0.4)
            lol.edit_text("𝗦𝗧𝗔𝗥𝗧𝗜𝗡𝗚 𝗕𝗢𝗧 𝗪𝗔𝗜𝗧..😇")
            time.sleep(0.4)
            lol.edit_text("𝗦𝗢𝗥𝗥𝗬 𝗙𝗢𝗥 𝗟𝗔𝗧𝗘......😍")
            time.sleep(0.4)
            lol.edit_text("sᴛᴀʀᴛɪɴɢ ʙᴏᴛ ᴍᴇʀɪ ᴊᴀᴀɴ...🥰")
            time.sleep(0.4)
            lol.edit_text("sᴛᴀʀᴛɪɴɢ ʜᴏ ʀᴀʜᴀ ʜᴀɪ......🥀")
            time.sleep(0.4)
            lol.edit_text("sᴛᴀʀᴛɪɴɢ ʜᴏ ʀᴀʜᴀ ʜᴀɪ.......💞")
            time.sleep(0.4)
            lol.edit_text("sᴛᴀʀᴛɪɴɢ ʜᴏ ʀᴀʜᴀ ʜᴀɪ........👀")
            time.sleep(0.4)
            lol.edit_text("sᴛᴀʀᴛɪɴɢ ʜᴏ ʀᴀʜᴀ ʜᴀɪ.........💫")
            time.sleep(0.4)
            lol.delete()
            
            update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ  !\n<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ​:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ​​* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


@run_async
def Mukesh_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "mukesh_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"*ʜᴇʏ,*🥀\n  *ᴛʜɪs ɪs {dispatcher.bot.first_name}*"
            "\n\n*ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ & ᴍᴜsɪᴄ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴜɪʟᴛ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴇᴀꜱɪʟʏ ᴀɴᴅ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ ꜰʀᴏᴍ ꜱᴄᴀᴍᴍᴇʀꜱ ᴀɴᴅ ꜱᴘᴀᴍᴍᴇʀꜱ.*"
            "\n*ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ sǫʟᴀʟᴄʜᴇᴍʏ ᴀɴᴅ ᴍᴏɴɢᴏᴅʙ ᴀs ᴅᴀᴛᴀʙᴀsᴇ.*"
            "\n➲  ɪ ᴄᴀɴ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ."
            "\n➲  ɪ ʜᴀᴠᴇ ᴀɴ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɴᴛɪ-ꜰʟᴏᴏᴅ ꜱʏꜱᴛᴇᴍ."
            "\n➲  ɪ ᴄᴀɴ ɢʀᴇᴇᴛ ᴜꜱᴇʀꜱ ᴡɪᴛʜ ᴄᴜꜱᴛᴏᴍɪᴢᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ᴀɴᴅ ᴇᴠᴇɴ ꜱᴇᴛ ᴀ ɢʀᴏᴜᴘ'ꜱ ʀᴜʟᴇꜱ."
            "\n➲  ɪ ᴄᴀɴ ᴡᴀʀɴ ᴜꜱᴇʀꜱ ᴜɴᴛɪʟ ᴛʜᴇʏ ʀᴇᴀᴄʜ ᴍᴀx ᴡᴀʀɴꜱ, ᴡɪᴛʜ ᴇᴀᴄʜ ᴘʀᴇᴅᴇꜰɪɴᴇᴅ ᴀᴄᴛɪᴏɴꜱ ꜱᴜᴄʜ ᴀꜱ ʙᴀɴ, ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴇᴛᴄ."
            "\n➲  ɪ ʜᴀᴠᴇ ᴀ ɴᴏᴛᴇ ᴋᴇᴇᴘɪɴɢ ꜱʏꜱᴛᴇᴍ, ʙʟᴀᴄᴋʟɪꜱᴛꜱ, ᴀɴᴅ ᴇᴠᴇɴ ᴘʀᴇᴅᴇᴛᴇʀᴍɪɴᴇᴅ ʀᴇᴘʟɪᴇꜱ ᴏɴ ᴄᴇʀᴛᴀɪɴ ᴋᴇʏᴡᴏʀᴅꜱ."
            "\n\n ☆............𝙱𝚈 » ʀσᴄкყ............☆",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⎯꯭‌✭𝆺꯭𝅥𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁✭", url=f"https://t.me/Itzz_me_innocentt"
                        ),
                        InlineKeyboardButton(
                            text="⎯꯭‌✭𝆺꯭𝅥ᴿᴱᴾᴼ .𓈀✔", 
                            url="https://t.me/friendship_forever_group143",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="mukesh_back"),
                    ],
                ]
            ),
        )
    elif query.data == "mukesh_back":
        first_name = update.effective_user.first_name 
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


@run_async
def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_text(
            text=f"""
 **👀𝗛𝗲𝘆 𝗕𝗮𝗯𝘆 🖤\n\n 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 {dispatcher.bot.first_name} 🍷\n\n𝗜 𝗔𝗺 𝗔𝗻 𝗔𝗱𝘃𝗮𝗻𝗰𝗲𝗱 𝗔𝗻𝗱 𝗦𝘂𝗽𝗲𝗿𝗳𝗮𝘀𝘁 𝗩𝗖 𝗣𝗹𝗮𝘆𝗲𝗿 𝗪𝗶𝘁𝗵 24𝘅7 𝗔𝗰𝘁𝗶𝘃𝗲 » 𝗙𝗼𝗿 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗔𝗻𝗱 𝗚𝗿𝗼𝘂𝗽𝘀\n\n𝗙𝗲𝗲𝗹 𝗟𝗮𝗴 𝗙𝗿𝗲𝗲 𝗧𝗼 𝗔𝗱𝗱 𝗠𝗲 𝗜𝗻 𝗬𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽 𝗔𝗻𝗱 𝗘𝗻𝗷𝗼𝘆 𝗦𝘂𝗽𝗲𝗿 𝗛𝗶𝗴𝗵 𝗤𝘂𝗮𝗹𝗶𝘁𝘆 𝗔𝘂𝗱𝗶𝗼 𝗔𝗻𝗱 𝗩𝗶𝗱𝗲𝗼\n\n☆............𝙱𝚈 » [ɪɴɴᴏᴄᴇɴᴛ](https://t.me/Itzz_me_innocentt)............☆ 💞** 
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        
                InlineKeyboardButton(
                    text="ᴀᴅᴍɪɴ",
                    callback_data="Music_1",
                ),
                InlineKeyboardButton(
                    text="ᴀᴜᴛʜ",
                    callback_data="Music_2",
                ),
            
                InlineKeyboardButton(
                    text="ʙʟᴏᴄᴋ",
                    callback_data="Music_3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ɢᴄᴀsᴛ",
                    callback_data="Music_4",
                ),
                InlineKeyboardButton(
                    text="ɢʙᴀɴ",
                    callback_data="Music_5",
                ),
                InlineKeyboardButton(
                    text="ʟʏʀɪᴄs",
                    callback_data="Music_6",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ᴘʟᴀʏʟɪsᴛ",
                    callback_data="Music_7",
                ),
                InlineKeyboardButton(
                    text="ᴠᴏɪᴄᴇ-ᴄʜᴀᴛ",
                    callback_data="Music_8",
                ),
            ],
            [
           
                InlineKeyboardButton(
                    text="ᴘʟᴀʏ",
                    callback_data="Music_9",
                ),
            
            
                InlineKeyboardButton(
                    text="sᴜᴅᴏ",
                    callback_data="Music_10",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="sᴛᴀʀᴛ",
                    callback_data="Music_11",
                ),
            ],
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="mukesh_back"),
                    ],
                ]
           ),
        )
    elif query.data == "Music_1":
        query.message.edit_text(
            text=f"*» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ «*"
            f"""


ᴊᴜsᴛ ᴀᴅᴅ ᴄ ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.

/pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.

/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.

/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.

/player : ɢᴇᴛ ᴀ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ.

/queue : sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_2":
        query.message.edit_text(
            text=f"*» ᴀᴜᴛʜ ᴜsᴇʀs «*"
            f"""

ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ʙᴏᴛ ᴡɪᴛʜᴏᴜᴛ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ. [ᴀᴅᴍɪɴs ᴏɴʟʏ]

/auth [ᴜsᴇʀɴᴀᴍᴇ] : ᴀᴅᴅ ᴀ ᴜsᴇʀ ᴛᴏ ᴀᴜᴛʜ ʟɪsᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.

/unauth [ᴜsᴇʀɴᴀᴍᴇ] : ʀᴇᴍᴏᴠᴇ ᴀ ᴀᴜᴛʜ ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ.

/authusers : sʜᴏᴡs ᴛʜᴇ ᴀᴜᴛʜ ᴜsᴇʀs ʟɪsᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴩ.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_3":
        query.message.edit_text(
            text=f"*» ʙʟᴀᴄᴋʟɪsᴛ ᴄʜᴀᴛ «*"
            f""" 

ʙʟᴀᴄᴋʟɪsᴛ ғᴇᴀᴛᴜʀᴇ [ᴏɴʟʏ ғᴏʀ sᴜᴅᴏᴇʀs]

/blacklistchat [ᴄʜᴀᴛ ɪᴅ] : ʙʟᴀᴄᴋʟɪsᴛ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.

/whitelistchat [ᴄʜᴀᴛ ɪᴅ] : ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ.

/blacklistedchat : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.


😤 ʙʟᴏᴄᴋ ᴜsᴇʀs:

/block [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴄʜᴜᴛɪʏᴀ] : sᴛᴀʀᴛs ɪɢɴᴏʀɪɴɢ ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ, sᴏ ᴛʜᴀᴛ ʜᴇ ᴄᴀɴ'ᴛ ᴜsᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs.

/unblock [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ.

/blockedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_4":
        query.message.edit_text(
            text=f"*» ʙʀᴏᴀᴅᴄᴀsᴛ ғᴇᴀᴛᴜʀᴇ «*"
            f"""

/broadcast , /gcast  [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs:

-pin : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.
-pinloud : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ sᴇɴᴅ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴛᴏ ᴛʜᴇ ᴍᴇᴍʙᴇʀs.
-user : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.
-assistant : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.
-nobot : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ..

ᴇxᴀᴍᴩʟᴇ: /broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_5":
        query.message.edit_text(
            text=f"*» ɢʙᴀɴ ғᴇᴀᴛᴜʀᴇ «*"
            f"""

/gban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴄʜᴜᴛɪʏᴀ] : ɢʟᴏʙᴀʟʟʏ ʙᴀɴs ᴛʜᴇ ᴄʜᴜᴛɪʏᴀ ғʀᴏᴍ ᴀʟʟ ᴛʜᴇ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛ ʜɪᴍ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.

/ungban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴs ᴛʜᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ.

/gbannedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇʀ ᴜsᴇʀs.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_6":
        query.message.edit_text(
            text=f"*» 𝙻𝚈𝚁𝙸𝙲𝚂 & 𝚂𝙷𝙰𝚈𝚁𝙸 𝙵𝙴𝙰𝚃𝚄𝚁𝙴𝚂 «*"
            f"""

/loop [ᴅɪsᴀʙʟᴇ/ᴇɴᴀʙʟᴇ] ᴏʀ [ʙᴇᴛᴡᴇᴇɴ 1:10] 
: ᴡʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙᴏᴛ ᴡɪʟʟ ᴩʟᴀʏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴩ ғᴏʀ 10 ᴛɪᴍᴇs ᴏʀ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏᴏᴩs.

/shuffle : sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs.

/seek : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.

/seekback : ʙᴀᴄᴋᴡᴀʀᴅ sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ᴛʜᴇ ɢɪᴠᴇɴ ᴅᴜʀᴀᴛɪᴏɴ.

/lyrics [sᴏɴɢ ɴᴀᴍᴇ] : sᴇᴀʀᴄʜ ʟʏʀɪᴄs ғᴏʀ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ sᴏɴɢ ᴀɴᴅ sᴇɴᴅ ᴛʜᴇ ʀᴇsᴜʟᴛs.

/shayri , /love , /gf , /bf : 𝙶𝙴𝚃 𝚂𝙷𝙰𝚈𝚁𝙸 𝙵𝙾𝚁 𝙲𝙾𝚄𝙿𝙻𝙴𝚂

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_7":
        query.message.edit_text(
            text=f"*» ᴩʟᴀʏʟɪsᴛs ғᴇᴀᴛᴜʀᴇ «*"
            f"""

/playlist : ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀs.

/deleteplaylist : ᴅᴇʟᴇᴛᴇ ᴀɴʏ sᴀᴠᴇᴅ ᴛʀᴀᴄᴋ ɪɴ ʏᴏᴜʀ ᴩʟᴀʏʟɪsᴛ.

/play : sᴛᴀʀᴛs ᴩʟᴀʏɪɴɢ ғʀᴏᴍ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴩʟᴀʏʟɪsᴛ ᴏɴ sᴇʀᴠᴇʀ.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_8":
        query.message.edit_text(
            text=f"*» ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs «*"
            f"""

/activevoice : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs ᴏɴ ᴛʜᴇ ʙᴏᴛ.
/activevideo : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs ᴏɴ ʙᴏᴛ.
/autoend [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ sᴛʀᴇᴀᴍ ᴀᴜᴛᴏ ᴇɴᴅ ɪғ ɴᴏ ᴏɴᴇ ɪs ʟɪsᴛᴇɴɪɴɢ.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_9":
        query.message.edit_text(
            text=f"*» ᴩʟᴀʏ ғᴇᴀᴛᴜʀᴇ «*"
            f"""

•c sᴛᴀɴᴅs ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴩʟᴀʏ.
•v sᴛᴀɴᴅs ғᴏʀ ᴠɪᴅᴇᴏ ᴩʟᴀʏ.
•force sᴛᴀɴᴅs ғᴏʀ ғᴏʀᴄᴇ ᴩʟᴀʏ.

/play ᴏʀ /vplay ᴏʀ /cplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.

/playforce ᴏʀ /vplayforce ᴏʀ /cplayforce : ғᴏʀᴄᴇ ᴩʟᴀʏ sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ.

/channelplay [ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] ᴏʀ [ᴅɪsᴀʙʟᴇ] : ᴄᴏɴɴᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀ ɢʀᴏᴜᴩ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʀᴀᴄᴋs ʙʏ ᴛʜᴇ ʜᴇʟᴩ ᴏғ ᴄᴏᴍᴍᴀɴᴅs sᴇɴᴛ ɪɴ ɢʀᴏᴜᴩ.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_10":
        query.message.edit_text(
            text=f"*» ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴡɪᴛʜ ʙᴏᴛ «*"
            f"""

🥶 ʜᴇʀᴏᴋᴜ :

/usage : sʜᴏᴡs ᴛʜᴇ ᴅʏɴᴏ ᴜsᴀɢᴇ ᴏғ ᴛʜᴇ ᴍᴏɴᴛʜ.

🤓 ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs:

/restart : ʀᴇsᴛᴀʀᴛs ʏᴏᴜʀ ʙᴏᴛ.

/update : ᴜᴩᴅᴀᴛᴇs ᴛʜᴇ ʙᴏᴛ ғʀᴏᴍ ᴛʜᴇ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ.

/speedtest : ᴄʜᴇᴄᴋ ʙᴏᴛ's sᴇʀᴠᴇʀ sᴩᴇᴇᴅ.

/maintenance [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴏғ ʏᴏᴜʀ ʙᴏᴛ.

/logger [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] : ʙᴏᴛ ᴡɪʟʟ sᴛᴀʀᴛ ʟᴏɢɢɪɴɢ ᴛʜᴇ ᴀᴄᴛɪᴠɪᴛɪᴇs ʜᴀᴩᴩᴇɴ ᴏɴ ʙᴏᴛ.

/logs [ɴᴜᴍʙᴇʀ ᴏғ ʟɪɴᴇs] : ɢᴇᴛ ʟᴏɢs ᴏғ ʏᴏᴜʀ ʙᴏᴛ [ᴅᴇғᴀᴜʟᴛ ᴠᴀʟᴜᴇ ɪs 100 ʟɪɴᴇs]


☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_11":
        query.message.edit_text(
            text=f"*» ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴡɪᴛʜ ʙᴏᴛ «*"
            f"""

/start : sᴛᴀʀᴛs ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ.

/help : ɢᴇᴛ ʜᴇʟᴩ ᴍᴇɴᴜ ᴡɪᴛʜ ᴇxᴩʟᴀɴᴀᴛɪᴏɴ ᴏғ ᴄᴏᴍᴍᴀɴᴅs.

/reboot : ʀᴇʙᴏᴏᴛs ᴛʜᴇ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ.

/settings : sʜᴏᴡs ᴛʜᴇ ɢʀᴏᴜᴩ sᴇᴛᴛɪɴɢs ᴡɪᴛʜ ᴀɴ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ɪɴʟɪɴᴇ ᴍᴇɴᴜ.

/sudolist : sʜᴏᴡs ᴛʜᴇ sᴜᴅᴏ ᴜsᴇʀs ᴏғ ᴍᴜsɪᴄ ʙᴏᴛ.

☆............𝙱𝚈 » [ʀσᴄкყ](https://t.me/ROCKY_ISS_BACK)............☆""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝐇𝐄𝐋𝐏",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "» 𝗖𝗵𝗼𝗼𝘀𝗲 𝗔𝗻 𝗢𝗽𝘁𝗶𝗼𝗻 𝗙𝗼𝗿 𝗚𝗲𝘁𝘁𝗶𝗻𝗴 𝗛𝗲𝗹𝗽🏘",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝗦𝘁𝗮𝗿𝘁 𝗜𝗻 𝗣𝗿𝗶𝘃𝗮𝘁𝗲",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="𝗢𝗽𝗲𝗻 𝗛𝗲𝗿𝗲",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="✯ вαϲк ✯", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs​",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


@run_async
def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != {OWNER_ID} and DONATION_LINK:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [VIP BOY](https://t.me/THE_VIP_BOY)"
                f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATION_LINK})",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendAnimation(
                f"@{SUPPORT_CHAT}",
                animation="https://te.legra.ph/file/731f6b26b2ef1501e35c7.mp4",
                caption=f"""
{dispatcher.bot.first_name}

╔═════ஜ۩۞۩ஜ═════╗

  🥀𝗠𝗔𝗗𝗘 𝗕𝗬 [𝗥𝗢𝗖𝗞𝗬](https://t.me/ROCKY_ISS_BACK)🥀
  
╚═════ஜ۩۞۩ஜ═════╝
""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    CommandHandler("test", test)
    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        Mukesh_about_callback, pattern=r"mukesh_"
    )
    Music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_"
    )

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(Music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    LOGGER.info("𝗕𝗢𝗧 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗨\n\n╔═════ஜ۩۞۩ஜ════╗\n\n♨️𝗠𝗔𝗗𝗘 𝗕𝗬 𝗥𝗢𝗖𝗞𝗬♨️\n\n╚═════ஜ۩۞۩ஜ════╝")
    updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
