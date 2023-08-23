from . import fields

from . import base


class MessageId(base.TelegramObject):
    message_id: base.String = fields.Field()
