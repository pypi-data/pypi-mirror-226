import asyncio
import asyncio.tasks
import functools
import itertools
import json
import logging
import typing
import warnings
from typing import Optional, Union

from aiohttp import web

from viber.bot import Bot
from .. import types
from ..utils import helper
from ..utils.exceptions import TimeoutWarning
from ..utils.payload import get_md_text
from viber.types import ReplyKeyboard

BOT_DISPATCHER_KEY = 'BOT_DISPATCHER'
RESPONSE_TIMEOUT = 55

log = logging.getLogger(__name__)


class WebhookRequestHandler(web.View):
    # TODO: verify update

    def get_dispatcher(self):
        dp = self.request.app[BOT_DISPATCHER_KEY]
        try:
            from viber import Bot, Dispatcher
            Dispatcher.set_current(dp)
            Bot.set_current(dp.bot)
        except RuntimeError:
            pass
        return dp

    async def parse_update(self):
        data = await self.request.json()
        return types.Update(**data)

    async def post(self):
        update = await self.parse_update()
        results = await self.process_update(update)
        response = self.get_response(results)

        if response:
            web_response = response.get_web_response()
        else:
            web_response = web.Response(text='ok')

        return web_response

    async def process_update(self, update):
        """
        Need respond in less than 60 seconds in to webhook.

        So... If you respond greater than 55 seconds webhook automatically respond 'ok'
        and execute callback response via simple HTTP request.

        :param update:
        :return:
        """
        dispatcher = self.get_dispatcher()
        loop = dispatcher.loop or asyncio.get_event_loop()

        # Analog of `asyncio.wait_for` but without cancelling task
        waiter = loop.create_future()
        timeout_handle = loop.call_later(RESPONSE_TIMEOUT, asyncio.tasks._release_waiter, waiter)
        cb = functools.partial(asyncio.tasks._release_waiter, waiter)

        fut = asyncio.ensure_future(dispatcher.updates_handler.notify(update), loop=loop)
        fut.add_done_callback(cb)

        try:
            try:
                await waiter
            except asyncio.CancelledError:
                fut.remove_done_callback(cb)
                fut.cancel()
                raise

            if fut.done():
                return fut.result()
            else:
                # context.set_value(WEBHOOK_CONNECTION, False)
                fut.remove_done_callback(cb)
                fut.add_done_callback(self.respond_via_request)
        finally:
            timeout_handle.cancel()

    def respond_via_request(self, task):
        """
        Handle response after 55 second.

        :param task:
        :return:
        """
        warnings.warn(f"Detected slow response into webhook. "
                      f"(Greater than {RESPONSE_TIMEOUT} seconds)\n"
                      f"Recommended to use 'async_task' decorator from Dispatcher for handler with long timeouts.",
                      TimeoutWarning)

        dispatcher = self.get_dispatcher()
        loop = dispatcher.loop or asyncio.get_event_loop()

        try:
            results = task.result()
        except Exception as e:
            loop.create_task(
                dispatcher.errors_handlers.notify(dispatcher, types.Update.get_current(), e))
        else:
            response = self.get_response(results)
            if response is not None:
                asyncio.ensure_future(response.execute_response(dispatcher.bot), loop=loop)

    def get_response(self, results):
        """
        Get response object from results.

        :param results: list
        :return:
        """
        if results is None:
            return None
        for result in itertools.chain.from_iterable(results):
            if isinstance(result, BaseResponse):
                return result


class BaseResponse:
    """
    Base class for webhook responses.
    """

    @property
    def method(self) -> str:
        """
        In all subclasses of that class you need to override this property

        :return: str
        """
        raise NotImplementedError

    def prepare(self) -> typing.Dict:
        """
        You need to override this method.

        :return: response parameters dict
        """
        raise NotImplementedError

    def cleanup(self) -> typing.Dict:
        """
        Cleanup response after preparing. Remove empty fields.

        :return: response parameters dict
        """
        return {k: v for k, v in self.prepare().items() if v is not None}

    def get_response(self):
        """
        Get response object

        :return:
        """
        return {'method': self.method, **self.cleanup()}

    def get_web_response(self):
        """
        Get prepared web response with JSON data.

        :return: :class:`aiohttp.web.Response`
        """
        return web.json_response(self.get_response(), dumps=json.dumps)

    async def execute_response(self, bot):
        """
        Use this method if you want to execute response as simple HTTP request.

        :param bot: Bot instance.
        :return:
        """
        method_name = helper.HelperMode.apply(self.method, helper.HelperMode.snake_case)
        method = getattr(bot, method_name, None)
        if method:
            return await method(**self.cleanup())
        return await bot.request(self.method, self.cleanup())

    async def __call__(self, bot=None):
        if bot is None:
            from aiogram import Bot
            bot = Bot.get_current()
        return await self.execute_response(bot)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self()


class StartResponse(BaseResponse):
    method = None

    __slots__ = ('text', 'markup', 'tracking_data')

    def __init__(
            self, text: str,
            markup: ReplyKeyboard = None,
            tracking_data: str = None,
    ):
        self.text = text
        self.markup = markup
        self.tracking_data = tracking_data

    def prepare(self):
        bot = Bot.get_current()
        if self.markup is None:
            keyboard = self.markup
        else:
            keyboard = self.markup.to_python()
        text = get_md_text(self.text, bot.parse_mode)
        return {
            'sender': {'name': bot.name, 'avatar': bot.avatar},
            'min_api_version': bot.min_api_version,
            'type': 'text',
            'text': text,
            'keyboard': keyboard,
            'tracking_data': self.tracking_data,
        }
