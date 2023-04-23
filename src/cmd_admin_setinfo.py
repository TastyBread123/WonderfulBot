from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from filters.chat_type import ChatTypeFilter

from database import get_admin_lvl, get_config_data, set_config_data, set_member_chat_info


router = Router()


# /title
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('title'))
async def set_chat_title(message: types.Message, command: CommandObject):
    """
    Изменение название чата на то, которое модератор указал в аргументе new\n
    Требуется 4+ уровень админки\n
    
    Аргументы:
    :new - новое название чата
    """

    admin_lvl = get_admin_lvl(message.chat.id, message.from_user.id)
    
    if admin_lvl == False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 4: return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
        
    new_title = command.args
    if new_title is None or new_title == False or new_title == '': return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */title <новое название>*!", parse_mode='Markdown')
                
    await message.chat.set_title(new_title)
    return await message.answer(f'🍩 Администратор @{message.from_user.username} изменил название беседы на <b>{new_title}</b>', parse_mode= "HTML")


# /description
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('desc', 'description'))
async def set_chat_description(message: types.Message, command: CommandObject):
    """
    Изменение описание чата на то, которое модератор указал в аргументе new\n
    Требуется 4+ уровень админки\n
    
    Аргументы:
    :new - новое описание чата
    """

    admin_lvl = get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 4: return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
        
    new_title = command.args
    if new_title is None or new_title == ' ' or new_title == '': return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */description <новое описание>*!", parse_mode='Markdown')

    await message.chat.set_description(new_title)
    return await message.answer(f'😱 Администратор <b>@{message.from_user.username}</b> изменил описание беседы на <b>{new_title}</b>', parse_mode= "HTML")


# /setwelcome
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setwelcome'))
async def set_chat_welcome(message: types.Message, command: CommandObject):
    """
    Изменение приветствие новых участников чата на то, которое модератор указал в аргументе new\n
    Требуется 4+ уровень админки\n
    
    Аргументы:
    :new - новое приветствие чата
    """

    admin_lvl = get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 4: return await message.reply('⚠️ *У вас нет 4-ого и выше уровня доступа!*', parse_mode='Markdown')

    old_welcome = get_config_data(message.chat.id)
    if old_welcome == False: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

    new_welcome = command.args
    if new_welcome is None or new_welcome == False or new_welcome == '': return await message.reply("⚠️ Неверный синтаксис!\n\n/setwelcome *<новое приветствие>*", parse_mode='Markdown')

    set_config_data(message.chat.id, 'welcome', new_welcome)
    return await message.answer(f'😒 Старое приветствие - <b>{old_welcome[1]}</b>\n😃 Новое приветствие - <b>{new_welcome}</b>\n\n😇 Изменил администратор @{message.from_user.username}', parse_mode= "HTML")


# /setrules
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setrules'))
async def set_chat_rules(message: types.Message, command: CommandObject):
    """
    Изменение правил чата на те, которые модератор указал в аргументе new\n
    Требуется 5+ уровень админки\n
    
    Аргументы:
    :new - новые правила чата
    """

    admin_lvl = get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 5: return await message.reply('⚠️ *У вас нет 5-ого и выше уровня доступа!*', parse_mode='Markdown')
        
    old_rules = get_config_data(message.chat.id)
    if old_rules == False: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

    new_rules = command.args
    if new_rules is None or new_rules == False or new_rules == '': return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */setrules <новые правила>*", parse_mode='Markdown')
    
    set_config_data(message.chat.id, 'rules', new_rules)
    return await message.answer(f'😒 Старые правила - <b>{old_rules[0]}</b>\n😃 Новые правила - <b>{new_rules}</b>\n\n😇 Изменил @{message.from_user.username}', parse_mode= "HTML")


# /setvip
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setvip'))
async def set_vip(message: types.Message, command: CommandObject):
    """
    Изменение статуса VIP на указанный в аргументе new_status у того, на чье сообщение ответил модератор\n
    Требуется 5+ уровень админки\n
    
    Аргументы:
    :new_status - новый статус VIP у пользователя (0/1)
    """

    admin_lvl = get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 5: return await message.reply('⚠️ *У вас нет 5-ого и выше уровня доступа!*', parse_mode='Markdown')
        
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы выдать или снять VIP статус отправителю!*', parse_mode='Markdown')

    admin_lvl_member = get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')
    
    give_vip = command.args
    if give_vip is None or give_vip == False or give_vip == '': return await message.reply('⚠️ Неверный синтаксис!\n\n*/setvip <1 - выдать/2 - забрать>*', parse_mode='Markdown')

    if give_vip == '0':
        set_member_chat_info(message.chat.id, message.reply_to_message.from_user.id, 'vip', '0')
        return await message.answer(f'💎 Администратор @{message.from_user.username} снял <b>VIP статус</b> пользователю @{message.reply_to_message.from_user.username}', parse_mode= "HTML")
    
    elif give_vip == '1':
        set_member_chat_info(message.chat.id, message.reply_to_message.from_user.id, 'vip', '1')         
        return await message.answer(f'💎 Администратор @{message.from_user.username} выдал <b>VIP статус</b> пользователю @{message.reply_to_message.from_user.username}', parse_mode= "HTML")
    
    return await message.reply('⚠️ *Неверный аргумент! 1 - выдать/2 - забрать!*', parse_mode='Markdown')


# /setnick
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setnick', 'snick'))
async def set_nick_member(message: types.Message, command: CommandObject):
    admin_lvl = get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 3: return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
    
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы изменить ник отправителя!*', parse_mode= "Markdown")

    admin_lvl_member = get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете наказать данного пользователя!*", parse_mode='Markdown')
    
    new_nick = command.args
    if new_nick is None or new_nick == False or new_nick == '': return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */setnick <новый ник>*!', parse_mode='Markdown')

    set_member_chat_info(message.chat.id, message.reply_to_message.from_user.id, 'nick', new_nick)
    return await message.answer(f'💡 Администратор <b>@{message.from_user.username}</b> изменил ник <b>@{message.reply_to_message.from_user.username}</b> на <b>{new_nick}</b>', parse_mode= "HTML")


# /setadmin
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('setadmin'))
async def set_admin(message: types.Message, command: CommandObject):
    admin_lvl = get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False: return None
    if admin_lvl is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if admin_lvl < 5: return await message.reply("⚠️ У вас нет 5-ого и выше уровня доступа!", parse_mode='Markdown')
    
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение пользователя чтобы назначить его на пост администратора!*', parse_mode='Markdown')
            
    newadmin_lvl = command.args
    if newadmin_lvl is None or newadmin_lvl == False or newadmin_lvl == '': return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */makeadmin <level>*!", parse_mode='Markdown')
    if newadmin_lvl.isdigit() == False: return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */makeadmin <уровень>! Аргумент <уровень> - число*!", parse_mode='Markdown')

    if int(newadmin_lvl) <= -1: return await message.reply("*Нельзя установить уровень меньше 0!*", parse_mode='Markdown')
    elif int(newadmin_lvl) >= 6: return await message.reply("*Нельзя установить уровень выше 5!*", parse_mode='Markdown')

    admin_lvl_member = get_admin_lvl(message.chat.id, message.reply_to_message.from_user.id)
    if admin_lvl_member >= admin_lvl: return await message.reply("⚠️ *Вы не можете повысить/снять данного пользователя!*", parse_mode='Markdown')

    set_member_chat_info(message.chat.id, message.reply_to_message.from_user.id, 'admin', newadmin_lvl)
    return await message.answer(f'👮 Главный Администратор @{message.from_user.username} назначил пользователя @{message.reply_to_message.from_user.username} <b>администратором {newadmin_lvl} уровня</b>', parse_mode= "HTML")
