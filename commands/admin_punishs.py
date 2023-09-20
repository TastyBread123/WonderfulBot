from time import time

from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest

from filters.chat_type import ChatTypeFilter
from database import get_admin_lvl, get_member_chat_info, add_user, is_user_exists_chat_db, change_warns

router = Router()

# /kick
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('kick'))
async def kick_member(message: types.Message):
    """
    Кик пользователя, на сообщение которого ответил модератор\n
    Требуется 1+ уровень админки
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)

    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы кикнуть отправителя!*', parse_mode='Markdown')

    admin_lvl_member = await get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    try: await message.chat.ban(message.reply_to_message.from_user.id, 30)
    except TelegramBadRequest: return await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode='Markdown')
             
    return await message.answer(f'😱 Модератор @{message.from_user.username} кикнул пользователя @{message.reply_to_message.from_user.username}', parse_mode= "HTML")


# /mute
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('mute'))
async def mute_member(message: types.Message, command: CommandObject):
    """
    Мут пользователя, на сообщение которого ответил модератор\n
    Требуется 1+ уровень админки\n
    
    Аргументы:
    :time - время в минутах, на которое замучивается пользователь
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)

    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 1: return await message.reply("⚠️ У вас нет 1-ого и выше уровня доступа!", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы замутить отправителя!*', parse_mode='Markdown')

    admin_lvl_member = await get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    mute_time = command.args
    if mute_time is None or mute_time == False or mute_time == '': return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */mute <время в минутах>*!", parse_mode='Markdown')

    new = {'can_send_messages': False, 'can_send_media_messages': False,'can_send_polls': False,'can_send_other_messages': False, 'can_add_web_page_previews': False}
    try: await message.chat.restrict(user_id = message.reply_to_message.from_user.id, permissions= new, until_date=int(time()) + int(mute_time)*60)
    except TelegramBadRequest: return await message.reply("❌ *Вы не можете замутить данного пользователя!*", parse_mode='Markdown')

    if int(mute_time) >= 1: return await message.answer(f'✅ Модератор @{message.from_user.username} замутил @{message.reply_to_message.from_user.username} на <b>{mute_time} минут</b>', parse_mode= "HTML")
    else: return await message.answer(f'✅ Модератор @{message.from_user.username} замутил @{message.reply_to_message.from_user.username} <b>навсегда</b>', parse_mode= "HTML")


# /unmute
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('unmute'))
async def unmute_member(message: types.Message):
    """
    Размут пользователя, на сообщение которого ответил модератор\n
    Требуется 1+ уровень админки\n
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)

    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы размутить отправителя!*', parse_mode='Markdown')

    admin_lvl_member = await get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

        
    new = {'can_send_messages': True, 'can_send_media_messages': True,'can_send_polls': True,'can_send_other_messages': True, 'can_add_web_page_previews': True}
    try: await message.chat.restrict(user_id = message.reply_to_message.from_user.id, permissions=new)
    except TelegramBadRequest: return await message.reply("❌ *Вы не можете размутить данного пользователя!*", parse_mode='Markdown')

    return await message.answer(f'✅ Модератор @{message.from_user.username} размутил @{message.reply_to_message.from_user.username}', parse_mode= "HTML")


# /ban
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('ban'))
async def ban_member(message: types.Message, command: CommandObject):
    """
    Бан пользователя, на сообщение которого ответил модератор. Если у пользователя VIP, то он не может быть забанен на 10+ дней\n
    Требуется 3+ уровень админки\n
    
    Аргументы:
    :time - время в днях, на которое банится пользователь
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 3: return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы забанить отправителя!*', parse_mode= "Markdown")

    admin_lvl_member = await get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    until_date = command.args
    if until_date is None or len(until_date.strip()) == 0: return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */ban <срок в днях>*!", parse_mode='Markdown')

    is_vip = await get_member_chat_info(message.chat.id, message.reply_to_message.from_user.id)
    if is_vip is not (None or False) and int(is_vip[5]) == 1 and int(until_date) > 10: return await message.reply('⚠️ Вы не можете забанить человека с VIP статусом более чем на 10 дней!')
    
    try: await message.chat.ban(message.reply_to_message.from_user.id, until_date=time() + int(until_date)*86400)
    except TelegramBadRequest: return await message.reply("❌ *Вы не можете забанить данного пользователя!*", parse_mode= "Markdown")
                
    if int(until_date) >= 1: return await message.answer(f'✅ Администратор @{message.from_user.username} забанил пользователя @{message.reply_to_message.from_user.username} на <b>{until_date} дней</b>', parse_mode= "HTML")                
    else: return await message.answer(f'✅ Администратор @{message.from_user.username} забанил пользователя @{message.reply_to_message.from_user.username} <b>навсегда</b>', parse_mode= "HTML")


# /unban
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('unban'))
async def unban_member(message: types.Message, command: CommandObject):
    """
    Разбан пользователя, чей ID указали в аргументе ID\n
    Требуется 3+ уровень админки
    
    Аргументы:
    :id - id пользователь для разбана
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 3: return await message.reply('⚠️ *У вас нет 3-его и выше уровня доступа!*', parse_mode='Markdown')

    unban_member_id = command.args
    if unban_member_id is None or unban_member_id == False or unban_member_id == '': return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */unban <user id>*", parse_mode='Markdown')

    await message.chat.unban(unban_member_id)
    return await message.answer(f'🥰 Модератор @{message.from_user.username} разбанил пользователя с ID <b>{unban_member_id}</b>', parse_mode= "HTML")


# /warn
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('warn'))
async def warn_member(message: types.Message):
    """
    Выдать предупреждению пользователю, на чье сообщение ответил модератор\n
    Требуется 3+ уровень админки
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)

    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 3: return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы выдать варн отправителю!*', parse_mode= "Markdown")

    admin_lvl_member = await get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')

    is_exist = await is_user_exists_chat_db(message.chat.id, message.reply_to_message.from_user.id)
    if is_exist == False: 
        await add_user(message.chat.id, (message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, 0, message.reply_to_message.from_user.first_name, 1, 0, 0, 0, 20, 0))
        return await message.answer(f'✅ Модератор @{message.from_user.username} <b>выдал предупреждение</b> пользователю @{message.reply_to_message.from_user.username}\nТекущее количество - 1', parse_mode= "HTML")

    warns = await change_warns(message.chat.id, message.reply_to_message.from_user.id, '+')
    return await message.answer(f'✅ Модератор @{message.from_user.username} <b>выдал предупреждение</b> пользователю @{message.reply_to_message.from_user.username}\nТекущее количество - {warns}', parse_mode= "HTML")


# /unwarn
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('unwarn'))
async def unwarn_member(message: types.Message):
    """
    Снять предупреждению пользователю, на чье сообщение ответил модератор\n
    Требуется 3+ уровень админки
    """

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 3: return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы снять варн отправителю!*', parse_mode= "Markdown")

    admin_lvl_member = await get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')
        
    total_warns = await get_member_chat_info(message.chat.id, message.reply_to_message.from_user.id)
    if total_warns is None or total_warns[4] <= 0: return await message.reply('⛔️ *У пользователя нет предупреждений!*', parse_mode='Markdown')

    total_warns = await change_warns(message.chat.id, message.reply_to_message.from_user.id, '-')
    return await message.answer(f'✅ Модератор @{message.from_user.username} снял предупреждение пользователю @{message.reply_to_message.from_user.username}\nУ пользователя осталось <b>{total_warns} предупреждений</b>', parse_mode= "HTML")
