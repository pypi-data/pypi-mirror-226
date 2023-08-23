from __future__ import annotations

import inspect
import re
from abc import abstractmethod
from contextlib import suppress
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any, Iterable, Optional, Union, Pattern

from viber import types
from viber.dispatcher.filters.filters import BoundFilter, Filter
from viber.types import CallbackQuery, Message
from viber.types import KeyboardButton, InlineKeyboardButton

UserIDArgumentType = Union[Iterable[str], str]


class Text(Filter):
    _default_params = (
        ('text', 'equals'),
        ('text_contains', 'contains'),
        ('text_startswith', 'startswith'),
        ('text_endswith', 'endswith'),
    )

    def __init__(self,
                 equals: Optional[Union[str, Iterable[str]]] = None,
                 contains: Optional[Union[str, Iterable[str]]] = None,
                 startswith: Optional[Union[str, Iterable[str]]] = None,
                 endswith: Optional[Union[str, Iterable[str]]] = None,
                 ignore_case=False):

        # Only one mode can be used. check it.
        check = sum(map(lambda s: s is not None, (equals, contains, startswith, endswith)))
        if check > 1:
            args = "' and '".join([arg[0] for arg in [('equals', equals),
                                                      ('contains', contains),
                                                      ('startswith', startswith),
                                                      ('endswith', endswith)
                                                      ] if arg[1] is not None])
            raise ValueError(f"Arguments '{args}' cannot be used together.")
        elif check == 0:
            raise ValueError(f"No one mode is specified!")

        equals, contains, endswith, startswith = (
            [v] if isinstance(v, str) else v
            for v in (equals, contains, endswith, startswith)
        )

        self.equals = equals
        self.contains = contains
        self.endswith = endswith
        self.startswith = startswith
        self.ignore_case = ignore_case

    @classmethod
    def validate(cls, full_config: dict[str, Any]):
        for param, key in cls._default_params:
            if param in full_config:
                return {key: full_config.pop(param)}

    async def check(self, obj: Union[Message, CallbackQuery]):
        if isinstance(obj, Message):
            text = obj.text or obj.caption or ''
        elif isinstance(obj, CallbackQuery):
            text = obj.data
        else:
            return False

        if self.ignore_case:
            text = text.lower()
            _pre_process_func = lambda s: str(s).lower()
        else:
            _pre_process_func = str

        # now check
        if self.equals is not None:
            equals = list(map(_pre_process_func, self.equals))
            return text in equals

        if self.contains is not None:
            contains = list(map(_pre_process_func, self.contains))
            return all(map(text.__contains__, contains))

        if self.startswith is not None:
            startswith = list(map(_pre_process_func, self.startswith))
            return any(map(text.startswith, startswith))

        if self.endswith is not None:
            endswith = list(map(_pre_process_func, self.endswith))
            return any(map(text.endswith, endswith))

        return False


class Command(Filter):
    def __init__(self, commands: Union[Iterable, str],
                 prefixes: Union[Iterable, str] = '/',
                 ignore_case: bool = True):

        if isinstance(commands, str):
            commands = (commands,)

        self.commands = list(map(str.lower, commands)) if ignore_case else commands
        self.prefixes = prefixes
        self.ignore_case = ignore_case

    @classmethod
    def validate(cls, full_config: dict[str, Any]) -> Optional[dict[str, Any]]:
        config = {}
        if 'commands' in full_config:
            config['commands'] = full_config.pop('commands')
        if config and 'commands_prefix' in full_config:
            config['prefixes'] = full_config.pop('commands_prefix')
        return config

    async def check(self, message: types.Message):
        return await self.check_command(message, self.commands, self.prefixes, self.ignore_case)

    @classmethod
    async def check_command(cls, message: types.Message, commands, prefixes, ignore_case=True):
        text = message.text
        if not text:
            return False

        full_command, *args_list = text.split(maxsplit=1)
        args = args_list[0] if args_list else None
        prefix, command = full_command[0], full_command[1:]

        if prefix not in prefixes:
            return False
        if (command.lower() if ignore_case else command) not in commands:
            return False

        return {'command': cls.CommandObj(command=command, prefix=prefix, args=args)}

    @dataclass
    class CommandObj:
        prefix: str = '/'
        command: str = ''
        args: str = field(repr=False, default=None)

        @property
        def text(self) -> str:
            line = self.prefix + self.command
            if self.args:
                line += ' ' + self.args
            return line


class Regexp(Filter):

    def __init__(self, regexp):
        if not isinstance(regexp, Pattern):
            regexp = re.compile(regexp, flags=re.IGNORECASE | re.MULTILINE)
        self.regexp = regexp

    @classmethod
    def validate(cls, full_config: dict[str, Any]):
        if 'regexp' in full_config:
            return {'regexp': full_config.pop('regexp')}

    async def check(self, obj: Union[Message, CallbackQuery]):
        if isinstance(obj, Message):
            content = obj.text or obj.caption or ''
        elif isinstance(obj, CallbackQuery) and obj.data:
            content = obj.data
        else:
            return False

        match = self.regexp.search(content)

        if match:
            return {'regexp': match}
        return False


class IDFilter(Filter):

    def __init__(self, user_id: UserIDArgumentType):
        self.user_id = self.extract_chat_ids(user_id)

    @classmethod
    def validate(cls, full_config: dict[str, Any]) -> Optional[dict[str, Any]]:
        result = {}
        if 'user_id' in full_config:
            result['user_id'] = full_config.pop('user_id')
        return result

    @staticmethod
    def extract_chat_ids(user_id: UserIDArgumentType) -> set[str]:
        if isinstance(user_id, str):
            return {user_id}
        if isinstance(user_id, Iterable):
            return {item for item in user_id}

    async def check(self, obj: Union[Message, CallbackQuery]):
        if isinstance(obj, Message):
            user_id = obj.from_user.id
        elif isinstance(obj, CallbackQuery):
            user_id = obj.from_user.id
        else:
            return False

        return user_id in self.user_id


class ExceptionsFilter(BoundFilter):
    key = 'exception'

    def __init__(self, exception):
        self.exception = exception

    async def check(self, update, exception):
        try:
            raise exception
        except self.exception:
            return True
        except:
            return False


class ContentTypeFilter(BoundFilter):
    key = 'content_types'
    required = True
    default = types.ContentTypes.TEXT

    def __init__(self, content_types):
        if isinstance(content_types, str):
            content_types = (content_types,)
        self.content_types = content_types

    async def check(self, message):
        return types.ContentType.ANY in self.content_types or \
               message.content_type in self.content_types


class StateFilter(BoundFilter):
    key = 'state'
    required = True
    ctx_state = ContextVar('user_state')

    def __init__(self, dispatcher, state):
        from viber.dispatcher.filters.state import State, StatesGroup
        from viber.dispatcher import Dispatcher

        self.dispatcher: Dispatcher = dispatcher

        states = []
        if not isinstance(state, (list, set, tuple, frozenset)) or state is None:
            state = [state, ]
        for item in state:
            # noinspection PyTypeChecker
            if isinstance(item, State):
                states.append(item.state)
            elif inspect.isclass(item) and issubclass(item, StatesGroup):
                states.extend(item.all_states_names)
            else:
                states.append(item)
        self.states = states

    @staticmethod
    def get_target_user_id(obj):
        return getattr(getattr(obj, 'from_user', None), 'id', None)

    async def check(self, obj):
        if '*' in self.states:
            return {'state': self.dispatcher.current_state()}

        try:
            state = self.ctx_state.get()
        except LookupError:
            user_id = self.get_target_user_id(obj)

            if user_id:
                state = await self.dispatcher.storage.get_state(user=user_id)
                self.ctx_state.set(state)
                if state in self.states:
                    return {'state': self.dispatcher.current_state(), 'raw_state': state}

        else:
            if state in self.states:
                return {'state': self.dispatcher.current_state(), 'raw_state': state}

        return False


# === my ===

class _ButtonFilter(BoundFilter):
    key = 'button'

    @abstractmethod
    def cast_button(self, button):
        """Cast button to string for matching"""

    @abstractmethod
    def cast_update(self, obj):
        """Cast update-obj to string for matching"""

    @staticmethod
    def make_regexp(text: str):
        return re.sub(r"\\{(.+?)\\}", r"(?P<\1>.+)", re.escape(text))

    def __init__(self, button):
        buttons_regexps = []
        if not isinstance(button, (list, tuple, set)):
            button = [button]

        for item in button:
            if isinstance(item, str):
                button_data = item
            else:
                button_data = self.cast_button(item)

            assert isinstance(button_data, str), f'Invalid data for {self.__class__.__name__} filter'
            buttons_regexps.append(self.make_regexp(button_data))

        self.buttons_regexps = buttons_regexps

    def check_one(self, obj, button_regexp: str) -> Optional[dict]:
        obj_data = self.cast_update(obj)
        with suppress(TypeError):
            match = re.fullmatch(button_regexp, obj_data)
            if match:
                return {'button': match.groupdict()}

    async def check(self, obj) -> Union[dict, bool]:
        for regexp in self.buttons_regexps:
            result = self.check_one(obj, regexp)
            if result:
                return result
        return False


class MessageButton(_ButtonFilter):

    def cast_button(self, button: Union[KeyboardButton, InlineKeyboardButton]):
        if isinstance(button, KeyboardButton):
            return button.text
        elif isinstance(button, InlineKeyboardButton):
            return button.callback_data
        raise ValueError('Bad button')

    def cast_update(self, obj: types.Message):
        return obj.text
