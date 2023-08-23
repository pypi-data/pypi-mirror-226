from __future__ import annotations

from typing import Optional, Union

# from aiogram.types import fields
from . import fields, base
from .contact import Contact
from .inline_keyboard import InlineKeyboardMarkup
from .message_id import MessageId
from .reply_keyboard import ReplyKeyboardMarkup
from .user import User
# from ..types import base
from ..utils import helper


class Message(base.TelegramObject):
    content_type: base.String = fields.Field()
    from_user: User = fields.Field(base=User)
    text: base.String = fields.Field()
    media: base.String = fields.Field()
    contact: Contact = fields.Field(base=Contact)

    async def reply(self,
                    text: base.String,
                    parse_mode: Optional[base.String] = None,
                    reply_markup: Union[ReplyKeyboardMarkup,
                    InlineKeyboardMarkup,
                    None] = None,
                    tracking_data: Optional[base.String] = None,
                    ) -> MessageId:
        """Only for compability. Like self.answer()"""
        return await self.answer(text, parse_mode, reply_markup, tracking_data)

    async def answer(self,
                     text: base.String,
                     parse_mode: Optional[base.String] = None,
                     reply_markup: Union[ReplyKeyboardMarkup,
                     InlineKeyboardMarkup,
                     None] = None,
                     tracking_data: Optional[base.String] = None,
                     ) -> MessageId:
        return await self.bot.send_message(
            chat_id=self.from_user.id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            tracking_data=tracking_data,
        )

    async def answer_photo(self,
                           media: base.String,
                           text: base.String,
                           parse_mode: Optional[base.String] = None,
                           reply_markup: Union[ReplyKeyboardMarkup,
                           InlineKeyboardMarkup,
                           None] = None,
                           tracking_data: Optional[base.String] = None,
                           ) -> MessageId:
        return await self.bot.send_picture(
            chat_id=self.from_user.id,
            media=media,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            tracking_data=tracking_data,
        )


class ContentType(helper.Helper):
    mode = helper.HelperMode.snake_case

    ANY = helper.Item()  # any
    TEXT = helper.Item()  # text
    PICTURE = helper.Item()  # picture
    CONTACT = helper.Item()  # contact
    FILE = helper.Item()  # file


class ContentTypes(helper.Helper):
    mode = helper.HelperMode.snake_case

    TEXT = helper.ListItem()  # text
    PICTURE = helper.ListItem()  # picture


class ParseMode(helper.Helper):
    mode = helper.HelperMode.lowercase

    MARKDOWN = helper.Item()
    HTML = helper.Item()
