import logging

from asyncio import run
from aiogram import Dispatcher, Bot

from configs.settings import token
from commands import command_routers
from events import event_routers



logging.basicConfig(level=logging.INFO)
bot = Bot(token, parse_mode='HTML')
dp = Dispatcher()

async def main():
    """Главный поток"""

    dp.include_routers(*command_routers, *event_routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "chat_member"])


if __name__ == '__main__':
    run(main())
