from . import base
from . import fields


class Contact(base.TelegramObject):
    name: base.String = fields.Field()
    phone_number: base.String = fields.Field()
