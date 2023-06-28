from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from filters.chat_type import ChatTypeFilter
from database import get_admin_lvl, add_user, is_user_exists_chat_db


router = Router()

# /reg
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('reg'))
async def reg_member(message: types.Message):
    """
    Зарегистрировать пользователя, на чье сообщение был ответ с данной командой\n
    Требуется 1+ уровень админки\n
    """

    get_admin = await get_admin_lvl(message.chat.id, message.from_user.id)
    if get_admin is None: return None
    if int(get_admin) < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы зарегистрировать отправителя!*', parse_mode='Markdown')
        
    data = await is_user_exists_chat_db(message.chat.id, message.reply_to_message.from_user.id)
    if data == False:
        user_info = (message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, 0, message.reply_to_message.from_user.first_name, 0, 0, 0, 0, 20, 0)
        await add_user(message.chat.id, user_info)
        return await message.answer(f'Модератор <b>@{message.from_user.username}</b> зарегистрировал пользователя <b>@{message.reply_to_message.from_user.username}</b>', parse_mode='HTML')
        
    elif data is None: return await message.reply('❌ *Ваша беседа не зарегистрирована!*', parse_mode='Markdown')

    return await message.reply('❌ *Пользователь уже зарегистрирован!*', parse_mode='Markdown')


# /clear
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('clear'))
async def clear_chat(message: types.Message, command: CommandObject):
    """
    Очистка quantity сообщений в чате\n
    Требуется 2+ уровень админки\n
    
    Аргументы:
    :quantity - количество сообщений для очистки
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl < 2: return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
    
    clear = command.args
    if clear is None or clear == False or clear == '' or clear.isdecimal == False: return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */clear <кол-во сообщений (больше 0)>*!', parse_mode='Markdown')
    
    message_id = message.message_id
    exceptions = 0
    i = 0
    while i < int(clear):
        try:
            message_id -= 1
            i += 1
            await message.chat.delete_message(message_id)
        
        except TelegramForbiddenError: return await message.answer(f'✅ Было удалено только <b>{i}</b> из <b>{clear}</b> сообщений из-за <b>ограничений Telegram</b>!', parse_mode= "HTML")
        
        except TelegramBadRequest:
            exceptions += 1
            if exceptions > 60:
                return await message.answer(f'✅ Было удалено только <b>{i}</b> из <b>{clear}</b> сообщений из-за <b>ограничений Telegram</b>!', parse_mode= "HTML")
            continue
    
    else: return await message.answer(f'✅ Были очищены все <b>{i}</b> из <b>{clear}</b> сообщений!', parse_mode= "HTML")
