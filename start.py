from aiogram import Router, types
from aiogram.filters.command import Command

from filters.chat_type import ChatTypeFilter
from configs.settings import admins_id
from database import add_user, is_user_exists_chat_db, get_config_data, create_chat_in_db

router = Router()


# /start
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('start'))
async def start(message: types.Message):
    """Осуществляет регистрацию пользователя при вводе команды. Если юзер уже зарегистрирован, то бот проводит 'авторизацию'"""
    
    if await is_user_exists_chat_db(message.chat.id, message.from_user.id) is False:
        result = await add_user(message.chat.id, (message.from_user.id, message.from_user.username, 0, message.from_user.first_name, 0, 0, 0, 0, 20, 0))
        if result == False: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")    
        return await message.reply("☑️ *Вы успешно зарегистрировались в беседе!*", parse_mode='Markdown')  
    
    return await message.reply("☑️ *Вы успешно авторизовались в беседе*!", parse_mode='Markdown')


# /startbot
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('startbot'))
async def startbot(message: types.Message):
    """Осуществляет создание чата, при условии, что отправитель состоит в списке администрации (admins_id)"""

    if message.from_user.id not in admins_id: return False

    data = await get_config_data(message.chat.id)     
    if data != False: return await message.reply('❌ Бот *уже* зарегистрирован в чате!', parse_mode='Markdown')
    await create_chat_in_db(message.chat.id, start_info=(message.from_user.id, message.from_user.username, 6, message.from_user.first_name, 0, 1, 0, 0, 20, 0))

    return await message.reply("✅ *Бот был успешно запущен в беседе! Вам были выданы права администратора 6 уровня и VIP статус*\n\n*❗️ Напутствие:\nНе забудьте сменить приветствие и правила*!", parse_mode='Markdown')
