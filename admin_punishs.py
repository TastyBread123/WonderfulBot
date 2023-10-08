from time import time

from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.markdown import hlink, hcode

from filters.chat_type import ChatTypeFilter
from database import get_member_chat_info, add_user, is_user_exists_chat_db, change_warns

router = Router()

# /kick
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('kick'))
async def kick_member(message: types.Message, command: CommandObject):
    """
    Кик пользователя, на сообщение которого ответил модератор

    Требуется 1+ уровень админки
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы кикнуть отправителя, или укажите ID!*', parse_mode='Markdown')

    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    else:
        if command.args.isdecimal() == False: return await message.reply('⚠️ *Вы ввели неправильный ID или в строке есть буквы!*', parse_mode='Markdown')
        user = await message.chat.get_member(int(command.args))
        user = user.user
    
    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != (False or None) and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    try: await message.chat.ban(user.id, 30)
    except TelegramBadRequest: return await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode='Markdown')
    return await message.answer(f'😱 Модератор {hlink(admin_info[3], message.from_user.url)} кикнул пользователя {hlink(member_info[3], user.url)}\n👤 ID пользователя: {hcode(user.id)}', parse_mode= "HTML")


# /mute
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('mute'))
async def mute_member(message: types.Message, command: CommandObject):
    """
    Мут пользователя, на сообщение которого ответил модератор

    Требуется 1+ уровень админки
    
    Аргументы:
    :time - время в минутах, на которое замучивается пользователь
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы замутить отправителя, или введите ID пользователя!*', parse_mode='Markdown')

    if message.reply_to_message is not None:
        mute_time = command.args
        if mute_time is None or mute_time.isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /mute id время (в минутах)*', parse_mode='Markdown')
        user = message.reply_to_message.from_user
    
    else:
        args = command.args.split(' ')
        if len(args) != 2 or args[0].isdecimal() == False or args[1].isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /mute id время (в минутах)*', parse_mode='Markdown')
        mute_time = args[1]
        user = await message.chat.get_member(int(args[0]))
        user = user.user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != False and member_info != None and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    new = {'can_send_messages': False, 'can_send_media_messages': False,'can_send_polls': False,'can_send_other_messages': False, 'can_add_web_page_previews': False}
    try: await message.chat.restrict(user_id=user.id, permissions=new, until_date=int(time()) + int(mute_time)*60)
    except TelegramBadRequest: return await message.reply("❌ *Вы не можете замутить данного пользователя!*", parse_mode='Markdown')

    if int(mute_time) >= 1: return await message.answer(f'😊 Модератор {hlink(admin_info[3], message.from_user.url)} замутил пользователя {hlink(member_info[3], user.url)} на <b>{mute_time} минут</b>\n👤 ID пользователя: {hcode(user.id)}', parse_mode= "HTML")
    else: return await message.answer(f'😊 Модератор {hlink(admin_info[3], message.from_user.url)} замутил пользователя {hlink(member_info[3], user.url)} навсегда\n👤 ID пользователя: {hcode(user.id)}', parse_mode= "HTML")


# /unmute
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('unmute'))
async def unmute_member(message: types.Message, command: CommandObject):
    """
    Размут пользователя, на сообщение которого ответил модератор

    Требуется 1+ уровень админки
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы размутить отправителя, или введите ID пользователя!*', parse_mode='Markdown')

    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    else:
        if command.args.isdecimal() == False: return await message.reply('⚠️ *Вы ввели неправильный ID или в строке есть буквы!*', parse_mode='Markdown')
        user = await message.chat.get_member(int(command.args))
        user = user.user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != (False or None) and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    new = {'can_send_messages': True, 'can_send_media_messages': True,'can_send_polls': True,'can_send_other_messages': True, 'can_add_web_page_previews': True}
    try: await message.chat.restrict(user_id=user.id, permissions=new)
    except TelegramBadRequest: return await message.reply("❌ *Вы не можете размутить данного пользователя!*", parse_mode='Markdown')
    return await message.answer(f'👍 Модератор {hlink(admin_info[3], message.from_user.url)} размутил пользователя {hlink(member_info[3], user.url)}\n👤 ID пользователя: {hcode(user.id)}', parse_mode= "HTML")


# /ban
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('ban'))
async def ban_member(message: types.Message, command: CommandObject):
    """
    Бан пользователя, на сообщение которого ответил модератор. Если у пользователя VIP, то он не может быть забанен на 10+ дней
    
    Требуется 3+ уровень админки
    
    Аргументы:
    :time - время в днях, на которое банится пользователь
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 3: return await message.reply("⚠️ *У вас нет 3-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы забанить отправителя, или укажите ID!*', parse_mode= "Markdown")

    if message.reply_to_message is not None:
        until_date = command.args
        if until_date is None or until_date.isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /ban id время (в днях)*', parse_mode='Markdown')
        user = message.reply_to_message.from_user
    
    else:
        args = command.args.split(' ')
        if len(args) != 2 or args[0].isdecimal() == False or args[1].isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /ban id время (в днях)*', parse_mode='Markdown')
        until_date = args[1]
        user = await message.chat.get_member(int(args[0]))
        user = user.user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != (False or None) and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')
    
    try: await message.chat.ban(user.id, until_date=time() + int(until_date)*86400)
    except TelegramBadRequest: return await message.reply(" *Вы не можете забанить данного пользователя!*", parse_mode= "Markdown")
                
    if int(until_date) >= 1: return await message.answer(f'😊 Модератор {hlink(admin_info[3], message.from_user.url)} забанил пользователя {hlink(member_info[3], user.url)} на <b>{until_date} день</b>\n👤 ID пользователя: {hcode(user.id)}', parse_mode= "HTML")
    else: return await message.answer(f'😊 Модератор {hlink(admin_info[3], message.from_user.url)} забанил пользователя {hlink(member_info[3], user.url)} навсегда\n👤 ID пользователя: {hcode(user.id)}', parse_mode= "HTML")


# /unban
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('unban'))
async def unban_member(message: types.Message, command: CommandObject):
    """
    Разбан пользователя, чей ID указали в аргументе ID\n
    Требуется 3+ уровень админки
    
    Аргументы:
    :id - id пользователь для разбана
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 3: return await message.reply("⚠️ *У вас нет 3-ого и выше уровня доступа!*", parse_mode='Markdown')
    if command.args is None or command.args.strip().isdigit() == False: return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */unban <user id>*", parse_mode='Markdown')

    await message.chat.unban(command.args, True)
    return await message.answer(f'👍 Модератор {hlink(admin_info[3], message.from_user.url)} разбанил пользователя с ID {hcode(command.args)}', parse_mode="HTML")


# /warn
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('warn'))
async def warn_member(message: types.Message, command: CommandObject):
    """
    Выдать предупреждению пользователю, на чье сообщение ответил модератор\n
    Требуется 3+ уровень админки
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 3: return await message.reply("⚠️ *У вас нет 3-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы выдать варн отправителю, или укажите ID!*', parse_mode= "Markdown")

    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    else:
        if command.args.isdecimal() == False: return await message.reply('⚠️ *Вы ввели неправильный ID или в строке есть буквы!*', parse_mode='Markdown')
        user = await message.chat.get_member(int(command.args))
        user = user.user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != (False or None) and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    is_exist = await is_user_exists_chat_db(message.chat.id, user.id)
    if is_exist == False: await add_user(message.chat.id, (user.id, user.username, 0, user.first_name, 1, 0, 0, 0, 20, 0))

    warns = await change_warns(message.chat.id, user.id, '+')
    return await message.answer(f'😊 Модератор {hlink(admin_info[3], message.from_user.url)} выдал предупреждение пользователю {hlink(member_info[3], user.url)}\n👤 ID пользователя: {hcode(user.id)}\n✅ Текущее количество: <b>{warns}</b>', parse_mode= "HTML")


# /unwarn
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('unwarn'))
async def unwarn_member(message: types.Message, command: CommandObject):
    """
    Снять предупреждению пользователю, на чье сообщение ответил модератор\n
    Требуется 3+ уровень админки
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 3: return await message.reply("⚠️ *У вас нет 3-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы снять варн отправителю, или укажите ID!*', parse_mode= "Markdown")

    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    else:
        if command.args.isdecimal() == False: return await message.reply('⚠️ *Вы ввели неправильный ID или в строке есть буквы!*', parse_mode='Markdown')
        user = await message.chat.get_member(int(command.args))
        user = user.user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != (False or None) and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    warns = await get_member_chat_info(message.chat.id, user.id)
    if warns is None or warns[4] <= 0: return await message.reply('⛔️ *У пользователя нет предупреждений!*', parse_mode='Markdown')

    warns = await change_warns(message.chat.id, user.id, '-')
    return await message.answer(f'😊 Модератор {hlink(admin_info[3], message.from_user.url)} снял предупреждение пользователю {hlink(member_info[3], user.url)}\n👤 ID пользователя: {hcode(user.id)}\n✅ Текущее количество: <b>{warns}</b>', parse_mode= "HTML")
