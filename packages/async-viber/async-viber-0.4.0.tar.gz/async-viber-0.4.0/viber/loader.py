from asyncio import new_event_loop, sleep

from aiohttp.web import Application, run_app

from viber.contrib.fsm_storage.mongo import MongoStorage
from viber.dispatcher.webhook import WebhookRequestHandler, BOT_DISPATCHER_KEY
from .bot import Bot
from .config import APP_URL, WEBHOOK_PATH, BOT_TOKEN, BOT_NAME, MONGO, APP_PORT
from .dispatcher import Dispatcher


async def set_webhook():
    url = APP_URL + WEBHOOK_PATH
    await sleep(1)
    await bot.set_webhook(url)


bot = Bot(BOT_TOKEN, BOT_NAME, parse_mode='html', min_api_version=10)
storage = MongoStorage(
    db_name=MONGO.DB,
    host=MONGO.HOST,
    username=MONGO.USER,
    password=MONGO.PASSWORD,
    port=MONGO.PORT,
)
dp = Dispatcher(bot, storage)
app = Application()
app.router.add_post(WEBHOOK_PATH, WebhookRequestHandler)
app[BOT_DISPATCHER_KEY] = dp
loop = new_event_loop()


def run():
    loop.create_task(set_webhook())
    run_app(app, loop=loop, port=APP_PORT)
