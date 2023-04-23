import asyncio
import aiogram
import cmd_start, cmd_info, cmd_getinfo, cmd_pins, event_text, cmd_entertainment, cmd_roleplay, cmd_admin_smth, cmd_admin_setinfo, cmd_admin_punishs

from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram import Router, types, Dispatcher

from database import is_user_exists_chat_db, get_config_data, add_user
from configs.settings import *
from filters.chat_type import ChatTypeFilter


bot = aiogram.Bot(token, parse_mode='HTML')

event_router = Router()
@event_router.chat_member(ChatTypeFilter(chat_type=["group", "supergroup"]), ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_event(event: types.ChatMemberUpdated):
    welcome = get_config_data(event.chat.id)
    if welcome:
        if is_user_exists_chat_db(event.chat.id, event.new_chat_member.user.id) == False:
            add_user(event.chat.id, (event.new_chat_member.user.id, event.new_chat_member.user.username, 0, event.new_chat_member.user.first_name, 0, 0, 0, 0, 20, 0))

        return await bot.send_message(event.chat.id, f"@{event.new_chat_member.user.username}\n<b>{welcome[1]}</b>")


# Главный поток
async def main():
    dp = Dispatcher()

    # Подключаем команды
    dp.include_routers(cmd_start.router, cmd_info.router, cmd_getinfo.router, cmd_pins.router, cmd_entertainment.router, cmd_roleplay.router, cmd_admin_smth.router, cmd_admin_setinfo.router, cmd_admin_punishs.router)
    # Пподключаем события
    dp.include_routers(event_router, event_text.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    print('Бот запущен')
    return await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member"])


if __name__ == '__main__':
    asyncio.run(main())
