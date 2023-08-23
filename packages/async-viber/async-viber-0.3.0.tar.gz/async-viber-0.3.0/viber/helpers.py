from typing import Awaitable

from .dispatcher import State
from .types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup

ReplyKeyboard = ReplyKeyboardMarkup | InlineKeyboardMarkup


def reply(
        msg: Message,
        text: str,
        markup: ReplyKeyboard | bool = None,
) -> Awaitable[Message]:
    return msg.answer(text, reply_markup=markup or None)


async def ask(
        state: State,
        msg: Message,
        text: str,
        markup: ReplyKeyboard | bool = None,
):
    await state.set()
    await reply(msg, text, markup)


async def get_photo_url(msg: Message) -> str:
    return msg.media
