from . import base, fields


class User(base.TelegramObject):
    id: base.String = fields.Field()
    name: base.String = fields.Field()
    language: base.String = fields.Field()
    country: base.String = fields.Field()
    api_version: base.Integer = fields.Field()
