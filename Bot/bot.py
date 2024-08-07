import asyncio 
import logging
from aiogram import Bot, Dispatcher

from core.settings import settings

from core.handlers import start


logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()
    dp.include_router(start.router)
     
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())