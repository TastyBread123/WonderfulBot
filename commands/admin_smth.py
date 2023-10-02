from aiogram import Router, types
from aiogram.utils.markdown import hlink, hcode
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.filters.command import Command, CommandObject

from filters.chat_type import ChatTypeFilter
from database import add_user, is_user_exists_chat_db, get_member_chat_info


router = Router()

# /reg
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('reg'))
async def reg_member(message: types.Message, command: CommandObject):
    """
    Зарегистрировать пользователя, на чье сообщение был ответ с данной командой\n
    Требуется 1+ уровень админки\n
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы зарегистрировать отправителя, или введите ID!*', parse_mode='Markdown')
    
    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    else:
        if command.args.isdecimal() == False: return await message.reply('⚠️ *Вы ввели неправильный ID или в строке есть буквы!*')
        user = await message.chat.get_member(int(command.args))
        user = user.user

    data = await is_user_exists_chat_db(message.chat.id, user.id)
    if not data:
        member_info = await add_user(message.chat.id, (user.id, user.username, 0, user.first_name, 0, 0, 0, 0, 20, 0))
        return await message.answer(f'😇 Модератор {hlink(admin_info[3], message.from_user.url)} зарегистрировал пользователя {hlink(member_info[3], user.url)}', parse_mode='HTML')

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

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 3: return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
    
    clear = command.args
    if clear is None or len(clear.strip()) <= 0 or not clear.isdecimal(): return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */clear <кол-во сообщений (больше 0)>*!', parse_mode='Markdown')
    
    message_id = message.message_id
    exceptions = 0
    i = 0
    while i < int(clear):
        try:
            message_id -= 1; i += 1
            await message.chat.delete_message(message_id)
        
        except TelegramForbiddenError: return await message.answer(f'✅ Администратор {hlink(admin_info[3], message.from_user.url)} очистил только {hcode(i)} из {hcode(clear)} сообщений из-за <b>ограничений Telegram</b>!', parse_mode= "HTML")
        except TelegramBadRequest:
            exceptions += 1
            if exceptions > 60: return await message.answer(f'✅ Администратор {hlink(admin_info[3], message.from_user.url)} очистил только {hcode(i)} из {hcode(clear)} сообщений из-за <b>ограничений Telegram</b>!', parse_mode= "HTML")
    
    else: 
        return await message.answer(f'✅ Администратор {hlink(admin_info[3], message.from_user.url)} очистил все {hcode(i)} из {hcode(clear)} сообщений!', parse_mode= "HTML")
