import json
import os


def get_user_list(config, key):
    with open("{}/MukeshRobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    LOGGER = True

    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    TOKEN = os.environ.get("TOKEN")
    OWNER_ID = os.environ.get("OWNER_ID")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME")
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT")
    JOIN_LOGGER = os.environ.get("JOIN_LOGGER")
    EVENT_LOGS = os.environ.get("EVENT_LOGS")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI")

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = os.environ.get("URL")

    SPAMWATCH_API = os.environ.get("SPAMWATCH_API")
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT")

    DRAGONS = get_user_list("elevated_users.json", "dragons")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    DEMONS = get_user_list("elevated_users.json", "demons")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")

    DONATION_LINK = os.environ.get("DONATION_LINK")
    CERT_PATH = None
    PORT = int(os.environ.get("PORT", 5000))

    DEL_CMDS = True
    STRICT_GBAN = True
    WORKERS = int(os.environ.get("WORKERS", 8))

    BAN_STICKER = os.environ.get("BAN_STICKER")
    ALLOW_EXCL = True

    ALLOW_CHATS = []

    CASH_API_KEY = os.environ.get("CASH_API_KEY")
    TIME_API_KEY = os.environ.get("TIME_API_KEY")
    WALL_API = os.environ.get("WALL_API")

    BL_CHATS = []
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
