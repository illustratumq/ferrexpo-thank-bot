from app.keyboards.inline.base import *

history_cb = CallbackData('rating', 'action')


def history_kb():
    next_bt = InlineKeyboardButton('➡', callback_data=history_cb.new(action='next'))
    prev_bt = InlineKeyboardButton('⬅', callback_data=history_cb.new(action='prev'))
    back = InlineKeyboardButton('Закрити', callback_data=history_cb.new(action='close'))
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [prev_bt, back, next_bt]
        ]
    )