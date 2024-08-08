import asyncio 
import logging
from aiogram import Bot, Dispatcher

from core.create_bot import bot, dp

from core.handlers import voice

logging.basicConfig(level=logging.INFO)

async def main():

    dp.include_router(voice.router)
     
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())