from aiogram import types 

def get_tts_kb():
    buttons = [
        [
        types.InlineKeyboardButton(text = "Voice", callback_data="voice")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard