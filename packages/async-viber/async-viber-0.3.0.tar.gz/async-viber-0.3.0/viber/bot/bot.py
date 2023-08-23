from __future__ import annotations

from typing import Optional, Union

from aiogram.utils.mixins import DataMixin, ContextInstanceMixin

from .base import BaseBot, api
from .. import types
from ..types import base
from ..utils.payload import generate_payload, get_md_text
import asyncio


class Bot(BaseBot, DataMixin, ContextInstanceMixin):

    async def _send_message(self,
                            receiver: base.String,
                            type: Optional[base.String] = None,
                            parse_mode: Optional[base.String] = None,
                            tracking_data: Optional[base.String] = None,
                            keyboard: Union[types.ReplyKeyboardMarkup,
                                            types.InlineKeyboardMarkup,
                                            None] = None,
                            **kwargs) -> types.MessageId:
        """
        The send_message API allows accounts to send messages to Viber users who subscribe to the account.
        Return message_token. Unique ID of the message

        Source: https://developers.viber.com/docs/api/rest-bot-api/#send-message

        :param receiver: Unique Viber user id. Subscribed valid user id
        :param type: Message type. Available message types: text, picture, video, file, location, contact, sticker, carousel content and url
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply. Max 4000 characters
        :param kwargs: additional params for message of given type
        """

        sender = {'name': self.name, 'avatar': self.avatar}
        min_api_version = self.min_api_version

        if 'text' in kwargs:
            kwargs['text'] = get_md_text(kwargs['text'], parse_mode or self.parse_mode)

        if keyboard is not None:
            keyboard = keyboard.to_python()

        payload = generate_payload(**locals(), **kwargs, exclude=['kwargs'])
        result = await self.request(api.Methods.SEND_MESSAGE, payload)
        return types.MessageId(message_id=result['message_token'])

    async def send_message(self,
                           chat_id: base.String,
                           text: base.String,
                           parse_mode: Optional[base.String] = None,
                           reply_markup: Union[types.ReplyKeyboardMarkup,
                                               types.InlineKeyboardMarkup,
                                               None] = None,
                           tracking_data: Optional[base.String] = None) -> types.MessageId:
        """
        Send text message to Viber users who subscribe to the account.
        Return message_token. Unique ID of the message

        Source: https://developers.viber.com/docs/api/rest-bot-api/#text-message

        :param reply_markup:
        :param chat_id: Unique Viber user id. Subscribed valid user id
        :param text: The text of the message. Max length 7,000 characters
        :param parse_mode: Send Markdown or HTML, if you want Viber apps to show bold, italic or other in your bot's message.
        :param tracking_data: Allow the account to track messages and user’s replies.
            Sent tracking_data value will be passed back with user’s reply. Max 4000 characters
        """

        return await self._send_message(
            receiver=chat_id,
            type='text',
            parse_mode=parse_mode,
            keyboard=reply_markup,
            tracking_data=tracking_data,
            text=text,
        )

    async def send_picture(self,
                           chat_id: base.String,
                           media: base.String,
                           text: base.String,
                           parse_mode: Optional[base.String] = None,
                           reply_markup: Union[types.ReplyKeyboardMarkup,
                                               types.InlineKeyboardMarkup,
                                               None] = None,
                           tracking_data: Optional[base.String] = None) -> types.MessageId:
        return await self._send_message(
            receiver=chat_id,
            type='picture',
            parse_mode=parse_mode,
            keyboard=reply_markup,
            tracking_data=tracking_data,
            media=media,
            text=text,
        )

    async def set_webhook(self,
                          url: base.String,
                          allowed_updates: Optional[list[base.String]] = None,
                          send_name: Optional[base.Boolean] = None,
                          send_photo: Optional[base.Boolean] = None,
                          ) -> Optional[list[base.String]]:
        """
        This webhook will be used for receiving callbacks and user messages from Viber.

        # Warning: you must have already running web-app for setting webhook.
        # (For this reason there is 'delay' parameter)

        Source: https://developers.viber.com/docs/api/rest-bot-api/#setting-a-webhook

        :param url: Account webhook URL to receive callbacks & messages from users
            Webhook URL must use SSL Note: Viber doesn’t support self signed certificates.
        :param allowed_updates: Indicates the types of Viber events that the account owner would like to be notified about.
            Don’t include this parameter in your request to get all events.
            Possible values: delivered, seen, failed, subscribed, unsubscribed and conversation_started.
        :param send_name: Indicates whether or not the bot should receive the user name. Default false
        :param send_photo: Indicates whether or not the bot should receive the user photo. Default false
        :param delay: Delay setting webhook until web-app is running (:return: None)
        :return: List of event types you will receive a callback for.
        """

        payload = {
            'url': url,
            'event_types': allowed_updates,
            'send_name': send_name,
            'send_photo': send_photo,
        }

        async def _set_webhook() -> list[base.String]:
            resp = await self.request(api.Methods.SET_WEBHOOK, payload)
            return resp['event_types']

        return await _set_webhook()
