from __future__ import annotations

from . import fields, base

MAX_ROW_WIDTH = 6


class InlineKeyboardButton(base.TelegramObject):
    text: base.String = fields.Field()
    url: base.String = fields.Field()
    callback_data: base.String = fields.Field()

    def __init__(self, text: base.String,
                 url: base.String = None,
                 callback_data: base.String = None):
        super().__init__(text=text,
                         url=url,
                         callback_data=callback_data)


class InlineKeyboardMarkup(base.TelegramObject):
    inline_keyboard: list[list[InlineKeyboardButton]] = fields.ListOfLists(base=InlineKeyboardButton)

    def __init__(self, row_width=3, inline_keyboard=None, **kwargs):
        if inline_keyboard is None:
            inline_keyboard = []

        conf = kwargs.pop('conf', {}) or {}
        conf['row_width'] = row_width

        super().__init__(**kwargs,
                         conf=conf,
                         inline_keyboard=inline_keyboard)

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
                self.inline_keyboard.append(row)
                row = []
        if len(row) > 0:
            self.inline_keyboard.append(row)
        return self

    def row(self, *args):
        btn_array = []
        for button in args:
            btn_array.append(button)
        self.inline_keyboard.append(btn_array)
        return self

    def insert(self, button):
        if self.inline_keyboard and len(self.inline_keyboard[-1]) < self.row_width:
            self.inline_keyboard[-1].append(button)
        else:
            self.add(button)
        return self

    def to_python(self) -> dict:
        keyboard = {
            "Type": "keyboard",
            "DefaultHeight": False,
            "Buttons": [],
        }

        for row in self.inline_keyboard:
            columns = MAX_ROW_WIDTH // len(row)
            for button in row:
                silent = False

                if button.callback_data:
                    action_type = 'reply'
                    text = button.text
                    action_body = button.callback_data
                elif button.url:
                    action_type = 'open-url'
                    text = button.text
                    action_body = button.url
                    silent = True
                else:
                    raise TypeError(f'Bad button: {button}')

                keyboard['Buttons'].append({
                    "Columns": columns,
                    "Text": text,
                    "ActionBody": action_body,
                    "ActionType": action_type,
                    "Silent": silent,
                })

        return keyboard
