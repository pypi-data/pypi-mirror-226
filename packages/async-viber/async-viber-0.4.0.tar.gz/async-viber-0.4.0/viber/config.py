import env

BOT_TOKEN = env.get("BOT_TOKEN")
BOT_NAME = env.get("BOT_NAME")
APP_URL = env.get("APP_URL")
APP_PORT = env.get("APP_PORT", 80)
WEBHOOK_PATH = env.get("WEBHOOK_PATH", "/bot")


class MONGO:
    _ = "MONGO_"
    DB = env.get(_ + "DB")
    HOST = env.get(_ + "HOST")
    USER = env.get(_ + "USER", "root")
    PASSWORD = env.get(_ + "PASSWORD")
    PORT = env.get(_ + "PORT", 27017)

