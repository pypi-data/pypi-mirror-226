from __future__ import annotations

import typing

from . import base, fields

MAX_ROW_WIDTH = 6


class KeyboardButton(base.TelegramObject):
    text: base.String = fields.Field()
    request_contact: base.Boolean = fields.Field()
    request_location: base.Boolean = fields.Field()

    def __init__(self, text: base.String,
                 request_contact: base.Boolean = None,
                 request_location: base.Boolean = None,
                 **kwargs):
        super().__init__(text=text,
                         request_contact=request_contact,
                         request_location=request_location,
                         **kwargs)


class ReplyKeyboardMarkup(base.TelegramObject):
    keyboard: list[list[KeyboardButton]] = fields.ListOfLists(base=KeyboardButton, default=[])
    resize_keyboard: base.Boolean = fields.Field()

    def __init__(self, keyboard: list[list[KeyboardButton]] = None,
                 resize_keyboard: base.Boolean = None,
                 row_width: base.Integer = 3):
        super().__init__(keyboard=keyboard,
                         resize_keyboard=resize_keyboard,
                         conf={'row_width': row_width})

    @property
    def row_width(self):
        return self.conf.get('row_width', 3)

    @row_width.setter
    def row_width(self, value):
        self.conf['row_width'] = value

    def add(self, *args):
        row = []
        for index, button in enumerate(args, start=1):
            row.append(button)
            if index % self.row_width == 0:
                self.keyboard.append(row)
                row = []
        if len(row) > 0:
            self.keyboard.append(row)
        return self

    def row(self, *args):
        btn_array = []
        for button in args:
            btn_array.append(button)
        self.keyboard.append(btn_array)
        return self

    def insert(self, button):
        if self.keyboard and len(self.keyboard[-1]) < self.row_width:
            self.keyboard[-1].append(button)
        else:
            self.add(button)
        return self

    def to_python(self) -> dict[str, typing.Any]:
        keyboard = {
            "Type": "keyboard",
            "DefaultHeight": not self.resize_keyboard,
            "Buttons": [],
        }

        for row in self.keyboard:
            columns = MAX_ROW_WIDTH // len(row)
            for button in row:
                action_type = 'reply'

                if isinstance(button, str):
                    text = button
                elif isinstance(button, KeyboardButton):
                    text = button.text
                    if button.request_contact:
                        action_type = 'share-phone'
                    if button.request_location:
                        action_type = 'location-picker'
                else:
                    raise TypeError(f'Bad button: {button}')

                keyboard['Buttons'].append({
                    "Columns": columns,
                    "Text": text,
                    "ActionBody": text,
                    "ActionType": action_type,
                })

        return keyboard
