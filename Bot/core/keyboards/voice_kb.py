from aiogram import types

def get_voice_kb() -> types.InlineKeyboardMarkup:
    buttons = [
        [
        types.InlineKeyboardButton(text = "Answer", callback_data="answer"),
        types.InlineKeyboardButton(text = "Get text", callback_data="text")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
