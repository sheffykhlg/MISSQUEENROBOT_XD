import json
import os


def get_user_list(config, key):
    with open("{}/MukeshRobot/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    LOGGER = True

    API_ID = os.environ.get("API_ID", "25912079")
    API_HASH = os.environ.get("API_HASH", "c127cd4b96f4c61ae9e5cb206fdd8f09")
    TOKEN = os.environ.get("TOKEN", "7081901018:AAHQDn99G8Tkx2RT7vyIy1gRaKwsf9s8zuw")
    OWNER_ID = os.environ.get("OWNER_ID", "7584759990")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "@lnnocentIdkaaa")

    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "TG_FRIENDSS")
    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)

    # MongoDB
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://Alisha:Alisha123@cluster0.yqcpftw.mongodb.net/?retryWrites=true&w=majority")

    # PostgreSQL (Neon)
    DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_gGsVek6a9qPZ@ep-cool-breeze-ai4gb7kh-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "postgresql://neondb_owner:npg_gGsVek6a9qPZ@ep-cool-breeze-ai4gb7kh-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

    # Start image
    START_IMG = os.environ.get("START_IMG", "")

    # Temp folder
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")

    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = os.environ.get("URL", None)

    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)

    DRAGONS = get_user_list("elevated_users.json", "dragons")
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    DEMONS = get_user_list("elevated_users.json", "demons")
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")

    DONATION_LINK = os.environ.get("DONATION_LINK", None)
    CERT_PATH = None
    PORT = int(os.environ.get("PORT", 5000))

    DEL_CMDS = True
    STRICT_GBAN = True
    WORKERS = int(os.environ.get("WORKERS", 8))

    BAN_STICKER = os.environ.get("BAN_STICKER", None)
    ALLOW_EXCL = True
    ALLOW_CHATS = []

    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    WALL_API = os.environ.get("WALL_API", None)

    BL_CHATS = []
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
