from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.markdown import hlink, hcode

from filters.chat_type import ChatTypeFilter
from database import get_config_data, set_config_data, set_member_chat_info, get_member_chat_info

router = Router()

# /title
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('title'))
async def set_chat_title(message: types.Message, command: CommandObject):
    """
    Изменение название чата на то, которое модератор указал в аргументе new

    Требуется 4+ уровень админки
    
    Аргументы:
    :new - новое название чата
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 4: return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
    if command.args is None or len(command.args.strip()) < 0: return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */title <новое название>*!", parse_mode='Markdown')

    await message.chat.set_title(command.args)
    return await message.answer(f'🍩 Администратор {hlink(admin_info[3], message.from_user.url)} изменил название беседы на {hcode(command.args)}', parse_mode= "HTML")


# /description
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('desc', 'description'))
async def set_chat_description(message: types.Message, command: CommandObject):
    """
    Изменение описание чата на то, которое модератор указал в аргументе new

    Требуется 4+ уровень админки
    
    Аргументы:
    :new - новое описание чата
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 4: return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
    if command.args is None or len(command.args.strip()) < 0: return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */desc <новое описание чата>*!", parse_mode='Markdown')

    await message.chat.set_description(command.args)
    return await message.answer(f'✏️ Администратор {hlink(admin_info[3], message.from_user.url)} изменил название беседы на {hcode(command.args)}', parse_mode= "HTML")


# /setwelcome
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setwelcome'))
async def set_chat_welcome(message: types.Message, command: CommandObject):
    """
    Изменение приветствие новых участников чата на то, которое модератор указал в аргументе new

    Требуется 4+ уровень админки
    
    Аргументы:
    :new - новое приветствие чата
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 4: return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
    if command.args is None or len(command.args.strip()) <= 0: return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */setwelcome <новое приветствие чата>*!", parse_mode='Markdown')

    old_welcome = await get_config_data(message.chat.id)
    new_welcome = command.args

    await set_config_data(message.chat.id, 'welcome', new_welcome)
    return await message.answer(f'📍 Модератор {hlink(admin_info[3], message.from_user.url)} изменил приветствие чата!\n\n😒 Старое приветствие: {hcode(old_welcome[1])}\n😃 Новое приветствие: {hcode(new_welcome)}', parse_mode= "HTML")


# /setrules
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setrules'))
async def set_chat_rules(message: types.Message, command: CommandObject):
    """
    Изменение правил чата на те, которые модератор указал в аргументе new

    Требуется 5+ уровень админки
    
    Аргументы:
    :new - новые правила чата
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 4: return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
    if command.args is None or len(command.args.strip()) < 0: return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */setwelcome <новое приветствие чата>*!", parse_mode='Markdown')
        
    old_rules = await get_config_data(message.chat.id)
    new_rules = command.args
    
    await set_config_data(message.chat.id, 'rules', new_rules)
    return await message.answer(f'🧸 Модератор {hlink(admin_info[3], message.from_user.url)} изменил правила чата!\n\n😒 Старые правила: {hcode(old_rules[0])}\n😃 Новые правила: {hcode(new_rules)}', parse_mode= "HTML")


# /setvip
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setvip'))
async def set_vip(message: types.Message, command: CommandObject):
    """
    Изменение статуса VIP на указанный в аргументе new_status у того, на чье сообщение ответил модератор
    
    Требуется 5+ уровень админки  
    
    Аргументы:  
    :new_status - новый статус VIP у пользователя (0/1)
    """

    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 5: return await message.reply("⚠️ *У вас нет 5-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы выдать или снять VIP статус отправителю, или введите ID!*', parse_mode='Markdown')

    if message.reply_to_message is not None:
        new_status = command.args
        if new_status is None or new_status.isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /setvip новый статус <(0 - снять | 1 - выдать)>*', parse_mode='Markdown')
        user = message.reply_to_message.from_user
    
    else:
        args = command.args.split(' ')
        if len(args) != 2 or args[0].isdecimal() == False or args[1].isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /setvip <id пользователя> <новый статус (0 - снять | 1 - выдать)>*', parse_mode='Markdown')
        new_status = args[1]
        user = await message.chat.get_member(int(args[0]))
        user = user.user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != False and member_info != None and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете изменить VIP статус данного пользователя!*", parse_mode='Markdown')
    if new_status != '0' and new_status != '1': return await message.reply('⚠️ *Неверный последний аргумент! 1 - выдать/2 - забрать!*', parse_mode='Markdown')
    
    await set_member_chat_info(message.chat.id, user.id, 'vip', new_status)
    return await message.answer(f'💎 Администратор {hlink(admin_info[3], message.from_user.url)} <b>{"выдал" if new_status == "1" else "снял"} VIP статус</b> пользователю {hlink(member_info[3], user.url)}', parse_mode= "HTML")


# /setnick
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setnick', 'snick'))
async def set_nick_member(message: types.Message, command: CommandObject):
    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 5: return await message.reply("⚠️ *У вас нет 5-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы изменить ник отправителю, или введите ID!*', parse_mode='Markdown')

    if message.reply_to_message is not None:
        new_status = command.args
        if new_status is None: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /setnick <новый ник>*', parse_mode='Markdown')
        user = message.reply_to_message.from_user
    
    else:
        args = command.args.split(' ')
        if len(args) != 2 or args[0].isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /setnick <id пользователя> <новый ник>*', parse_mode='Markdown')
        new_status = args[1]
        user = await message.chat.get_member(int(args[0]))
        user = user.user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != False and member_info != None and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете изменить ник данного пользователя!*", parse_mode='Markdown')

    await set_member_chat_info(message.chat.id, user.id, 'nick', new_status)
    return await message.answer(f'💡 Администратор {hlink(admin_info[3], message.from_user.url)} <b>изменил</b> ник пользователю {hlink(member_info[3], user.url)}\n👤 ID пользователя: {hcode(user.id)}\n🖥 Новый ник: {hcode(new_status)}', parse_mode= "HTML")


# /setadmin
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setadmin'))
async def set_admin(message: types.Message, command: CommandObject):
    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_info[2] < 5: return await message.reply("⚠️ *У вас нет 5-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None and command.args is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы выдать или снять права администратора отправителю, или введите ID!*', parse_mode='Markdown')

    if message.reply_to_message is not None:
        new_status = command.args
        if new_status is None or new_status.isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /setadmin <уровень админки>*', parse_mode='Markdown')
        user = message.reply_to_message.from_user
    
    else:
        args = command.args.split(' ')
        if len(args) != 2 or args[0].isdecimal() == False or args[1].isdecimal() == False: return await message.reply('⚠️ *Вы неверно используете команду!\nПравильное использование: /setadmin <id пользователя> <уровень админки>*', parse_mode='Markdown')
        new_status = args[1]
        user = await message.chat.get_member(int(args[0]))
        user = user.user

    if admin_info[2] <= int(new_status): return await message.reply(f'⚠️ *Вы можете выдать лишь админку с 0 по {int(admin_info[2]) - 1} уровня*', parse_mode='Markdown')
    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info != False and member_info != None and member_info[2] >= admin_info[2]: return await message.reply("❌ *Вы не можете изменить права данного пользователя!*", parse_mode='Markdown')

    await set_member_chat_info(message.chat.id, user.id, 'admin', new_status)
    return await message.answer(f'👮 Администратор {hlink(admin_info[3], message.from_user.url)} <b>изменил</b> уровень админ-прав пользователю {hlink(member_info[3], user.url)}\n👤 ID пользователя: {hcode(user.id)}\n🫡 Новый уровень: {hcode(new_status)}', parse_mode= "HTML")
