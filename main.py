import logging

from asyncio import run
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram import Router, types, Dispatcher, Bot

from database import is_user_exists_chat_db, get_config_data, add_user
from configs.settings import *
from filters.chat_type import ChatTypeFilter
from commands import command_routers
from events import event_routers


logging.basicConfig(level=logging.INFO)
bot = Bot(token, parse_mode='HTML')
on_member_router = Router()


@on_member_router.chat_member(ChatTypeFilter(chat_type=["group", "supergroup"]), ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_event(event: types.ChatMemberUpdated):
    welcome = get_config_data(event.chat.id)
    if welcome:
        if is_user_exists_chat_db(event.chat.id, event.new_chat_member.user.id) == False:
            add_user(event.chat.id, (event.new_chat_member.user.id, event.new_chat_member.user.username, 0, event.new_chat_member.user.first_name, 0, 0, 0, 0, 20, 0))

        return await bot.send_message(event.chat.id, f"@{event.new_chat_member.user.username}\n<b>{welcome[1]}</b>")


# Главный поток
async def main():
    dp = Dispatcher()

    # Подключаем роутеры
    for i in command_routers: dp.include_router(i)
    for i in event_routers: dp.include_router(i)
    dp.include_router(on_member_router)

    await bot.delete_webhook(drop_pending_updates=True)
    return await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member"])


if __name__ == '__main__':
    run(main())
