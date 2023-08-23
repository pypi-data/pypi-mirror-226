from __future__ import annotations

from typing import Union, Optional, TYPE_CHECKING

from aiogram.dispatcher.middlewares import MiddlewareManager
from aiogram.utils.mixins import DataMixin, ContextInstanceMixin
from viber import types
from viber.bot import Bot
from viber.dispatcher.filters.builtin import (
    Text,
    Regexp,
    IDFilter,
    Command,
    StateFilter,
    ContentTypeFilter,
    ExceptionsFilter,
    MessageButton,
)
from viber.dispatcher.filters.factory import FiltersFactory, Handler
from viber.dispatcher.storage import DisabledStorage, BaseStorage, FSMContext
from viber.types import Update

if TYPE_CHECKING:
    from .filters.state import State


class _Dispatcher(DataMixin, ContextInstanceMixin):

    def __init__(self, bot: Bot, storage: BaseStorage = None, loop=None):
        if storage is None:
            storage = DisabledStorage()

        self.bot = bot
        self.storage = storage
        self._main_loop = loop

        self.updates_handler = Handler(self, middleware_key='update')
        self.message_handlers = Handler(self, middleware_key='message')
        self.conversation_started_handlers = Handler(self, middleware_key='conversation_started')
        self.callback_query_handlers = Handler(self, middleware_key='callback_query')
        self.errors_handlers = Handler(self, once=False, middleware_key='error')

        self.updates_handler.register(self.process_update)

        self.filters_factory = FiltersFactory(self)
        self.middleware = MiddlewareManager(self)

        self._setup_filters()

    @property
    def loop(self):
        return self._main_loop

    def _setup_filters(self):
        filters_factory = self.filters_factory

        filters_factory.bind(StateFilter, exclude_event_handlers=[
            self.errors_handlers,
        ])

        filters_factory.bind(ContentTypeFilter, event_handlers=[
            self.message_handlers,
        ]),

        filters_factory.bind(Command, event_handlers=[
            self.message_handlers,
        ])

        filters_factory.bind(Text, event_handlers=[
            self.message_handlers,
            self.callback_query_handlers,
        ])

        filters_factory.bind(Regexp, event_handlers=[
            self.message_handlers,
            self.callback_query_handlers,
        ])

        filters_factory.bind(ExceptionsFilter, event_handlers=[
            self.errors_handlers,
        ])

        filters_factory.bind(IDFilter, event_handlers=[
            self.message_handlers,
            self.callback_query_handlers,
        ])

        filters_factory.bind(MessageButton, event_handlers=[
            self.message_handlers,
        ])

    def current_state(self, *, user: Union[str, int, None] = None) -> FSMContext:
        if user is None:
            user_obj = types.User.get_current()
            user = user_obj.id if user_obj else None

        return FSMContext(storage=self.storage, user=user)


# from aiogram import Dispatcher


class Dispatcher(_Dispatcher):

    def __init__(self, bot: Bot, storage: BaseStorage = None, loop=None):
        super().__init__(bot, storage, loop)

    def register_message_handler(self, callback, *custom_filters, commands=None, regexp=None, content_types=None,
                                 state=None, **kwargs):
        filters_set = self.filters_factory.resolve(self.message_handlers,
                                                   *custom_filters,
                                                   commands=commands,
                                                   regexp=regexp,
                                                   content_types=content_types,
                                                   state=state,
                                                   **kwargs)
        self.message_handlers.register(callback, filters_set)

    def message_handler(self, *custom_filters, commands=None, regexp=None, content_types=None, state=None,
                        **kwargs):
        def decorator(callback):
            self.register_message_handler(callback, *custom_filters,
                                          commands=commands, regexp=regexp, content_types=content_types,
                                          state=state, **kwargs)
            return callback

        return decorator

    def register_conversation_started_handler(self, callback, *custom_filters, **kwargs):
        filters_set = self.filters_factory.resolve(self.conversation_started_handlers,
                                                   *custom_filters,
                                                   **kwargs)
        self.conversation_started_handlers.register(callback, filters_set)

    def conversation_started_handler(self, *custom_filters, **kwargs):
        def decorator(callback):
            self.register_conversation_started_handler(callback, *custom_filters, **kwargs)
            return callback

        return decorator

    async def process_update(self, update: Update):
        print(update)
        types.Update.set_current(update)

        try:
            if update.message:
                types.Message.set_current(update.message)
                types.User.set_current(update.message.from_user)
                return await self.message_handlers.notify(update.message)
            if update.conversation_started:
                types.ConversationStarted.set_current(update.conversation_started)
                types.User.set_current(update.conversation_started.from_user)
                return await self.conversation_started_handlers.notify(update.conversation_started)
        except Exception as e:
            err = await self.errors_handlers.notify(update, e)
            if err:
                return err
            raise

    def start(self, state: str | State | None = "*"):
        return self.conversation_started_handler(state=state)

    def text(self, button: str = None):
        return TextHandler(self, button)

    def contact(self):
        return ContactHandler(self)

    def photo(self):
        return PictureHandler(self)

    def document(self):
        return FileHandler(self)

    button = text

    @property
    def START(self):  # noqa
        return self.start()

    @property
    def TEXT(self):  # noqa
        return self.text()

    @property
    def CONTACT(self):  # noqa
        return self.contact()

    @property
    def PHOTO(self):  # noqa
        return self.photo()

    @property
    def DOCUMENT(self):  # noqa
        return self.document()


class _Handler:
    def __init__(self, dp: Dispatcher):
        self._dp = dp
        self._state = None
        self._user_id = None
        self._extra = {}

    def state(self, value: str | State | None = "*"):
        self._state = value
        return self

    def user_id(self, value: int):
        self._user_id = value
        return self

    def extra(self, **kwargs):
        self._extra = kwargs
        return self

    def __call__(self, callback):
        raise NotImplementedError


class MessageHandler(_Handler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)
        self._command = None
        self._text = None
        self._content_types = None

    def __call__(self, callback):
        deco = self._dp.message_handler(
            content_types=self._content_types,
            button=self._text,
            commands=self._command,
            state=self._state,
            user_id=self._user_id,
            **self._extra,
        )
        return deco(callback)


class TextHandler(MessageHandler):
    def __init__(self, dp: Dispatcher, text: str):
        super().__init__(dp)
        self._text = text


class ContactHandler(MessageHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)
        self._content_types = "contact"


class FileHandler(MessageHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)
        self._content_types = "file"


class PictureHandler(MessageHandler):
    def __init__(self, dp: Dispatcher):
        super().__init__(dp)
        self._content_types = "picture"
