from __future__ import annotations

from . import fields, base
from .user import User


class ConversationStarted(base.TelegramObject):
    action_type: base.String = fields.Field()
    from_user: User = fields.Field(base=User)
    subscribed: base.Boolean = fields.Field()
