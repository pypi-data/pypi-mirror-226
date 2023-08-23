from __future__ import annotations

from copy import deepcopy

from .types import InlineKeyboardButton, KeyboardButton


class InlineButton(InlineKeyboardButton):
    def format(self, *args, **kwargs) -> InlineButton:
        button = deepcopy(self)
        for attr, value in button.values.items():
            if isinstance(value, str):
                button[attr] = value.format(*args, **kwargs)
        return button


class CallbackButton(InlineButton):
    def __init__(self, text: str, data: str = None):
        super().__init__(text, callback_data=data or text)


class UrlButton(InlineButton):
    def __init__(self, text: str, url: str):
        super().__init__(text, url=url)


class ContactRequestButton(KeyboardButton):
    def __init__(self, text: str):
        super().__init__(text, request_contact=True)
