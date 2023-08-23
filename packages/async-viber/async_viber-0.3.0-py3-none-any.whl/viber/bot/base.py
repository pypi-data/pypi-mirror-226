import asyncio
import json
import ssl
import typing
from typing import Dict, List, Optional, Union, Type

import aiohttp
import certifi
from aiogram.types import ParseMode

from . import api
from ..types import ParseMode, base


class BaseBot:

    def __init__(
            self,
            token: base.String,
            name: base.String,
            avatar: base.String = None,
            min_api_version: base.Integer = None,
            loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None,
            parse_mode: typing.Optional[base.String] = None,
    ):
        self._main_loop = loop
        self._token = token

        self.name = name
        self.avatar = avatar
        self.min_api_version = min_api_version

        # aiohttp main session
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        self._session: Optional[aiohttp.ClientSession] = None
        self._connector_class: Type[aiohttp.TCPConnector] = aiohttp.TCPConnector
        self._connector_init = dict(limit=None, ssl=ssl_context)

        if parse_mode is not None:
            if not isinstance(parse_mode, str):
                raise TypeError(f"Parse mode must be str, not {type(parse_mode)}")
            parse_mode = parse_mode.lower()
            if parse_mode not in ParseMode.all():
                raise ValueError(f"Parse mode must be one of {ParseMode.all()}")

        self.parse_mode = parse_mode

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            connector=self._connector_class(**self._connector_init, loop=self._main_loop),
            loop=self._main_loop,
            json_serialize=json.dumps
        )

    @property
    def loop(self) -> Optional[asyncio.AbstractEventLoop]:
        return self._main_loop

    @property
    def session(self) -> Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = self.get_new_session()
        return self._session

    async def request(self, method: base.String,
                      data: Optional[Dict] = None, **kwargs) -> Union[List, Dict, base.Boolean]:
        return await api.make_request(self.session, self._token, method, data, **kwargs)
