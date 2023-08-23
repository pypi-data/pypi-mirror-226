from __future__ import annotations

import copy
from typing import Any

from . import base, fields
from .conversation_started import ConversationStarted
from .message import Message


class Update(base.TelegramObject):
    event: base.String = fields.Field()
    timestamp: base.Integer = fields.DateTimeField()
    chat_hostname: base.String = fields.Field()
    message_token: base.Integer = fields.Field()
    silent: base.Boolean = fields.Field()
    type: base.String = fields.Field()

    message: Message = fields.Field(base=Message)
    conversation_started: ConversationStarted = fields.Field(base=ConversationStarted)

    @staticmethod
    def transform_message(raw_data: dict):
        new_data = copy.deepcopy(raw_data)
        message = new_data['message']

        from_user = new_data.pop('sender')
        message['from_user'] = from_user
        message['content_type'] = message.pop('type')
        return new_data

    @staticmethod
    def transform_conversation_started(raw_data: dict):
        new_data = copy.deepcopy(raw_data)
        cs = new_data['conversation_started'] = {}

        cs['from_user'] = new_data.pop('user')
        cs['action_type'] = new_data.pop('type')
        cs['subscribed'] = new_data.pop('subscribed')
        return new_data

    def __init__(self, conf: dict[str, Any] = None, **kwargs: Any) -> None:
        if 'timestamp' in kwargs:  # fix timestamp
            kwargs['timestamp'] /= 1000

        if kwargs['event'] == 'message':
            kwargs = self.transform_message(kwargs)

        if kwargs['event'] == 'conversation_started':
            kwargs = self.transform_conversation_started(kwargs)

        super().__init__(conf, **kwargs)
