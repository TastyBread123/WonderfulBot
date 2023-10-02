from aiogram import Router, types
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.markdown import hlink, hcode

from filters.chat_type import ChatTypeFilter
from database import get_member_chat_info, get_admin_lvl, get_config_data


router = Router()

# /getid
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('getid', 'gid'))
async def get_member_id(message: types.Message):
    if message.reply_to_message is None: return await message.answer('⚠️ *Ответьте на сообщение пользователя чтобы узнать его ID!*', parse_mode='Markdown')
    return await message.answer(f'🔍 ID {hlink("пользователя", message.reply_to_message.from_user.url)} - {hcode(message.reply_to_message.from_user.id)}', parse_mode="HTML")


# /checkvip
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("checkvip"))
async def get_member_vip(message: types.Message, command: CommandObject):
    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    elif command.args is not None:
        if command.args.isdecimal():
            user = await message.chat.get_member(int(command.args))
            user = user.user
        else: return await message.reply('⚠️ <b>Вы ввели неверный ID пользователя!</b>')
    else: user = message.from_user

    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl < 1 or admin_lvl is None or admin_lvl == False: return await message.reply('⚠️ *У вас нет 1-ого и выше уровня доступа!*', parse_mode='Markdown')

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode="Markdown")
    
    if member_info[5]: return await message.reply(f'😍 У пользователя {hlink(member_info[3], user.url)} имеется VIP статус')
    else: return await message.reply(f'😔 У пользователя {hlink(member_info[3], user.url)} отсутствует VIP статус')


# /stats
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('user', 'profile', 'stats'))
async def statistic_member(message: types.Message, command: CommandObject):
    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    elif command.args is not None:
        if command.args.isdecimal():
            user = await message.chat.get_member(int(command.args))
            user = user.user
        else: return await message.reply('⚠️ <b>Вы ввели неверный ID пользователя!</b>')
    else: user = message.from_user
      
    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode="Markdown")
    elif member_info == False: return await message.reply('⚠️ Пользователь не зарегистрирован!*', parse_mode= "Markdown")
    
    return await message.reply(f'<b>{"👑" if member_info[5] else "👤"} Профиль {hlink(member_info[3], user.url)} [{hcode(member_info[0])}]</b>\n\n🎓 Количество варнов - <b>{member_info[4]}</b>\n\n🔑 Уровень - <b>{member_info[9]}</b>. Всего - <b>{member_info[6]} EXP</b>\n🎉 До нового уровня - <b>{member_info[7]} EXP из {member_info[8]} EXP</b>', parse_mode= "HTML")


# /rank
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('rank'))
async def rank_member(message: types.Message, command: CommandObject):
    if message.reply_to_message is not None: user = message.reply_to_message.from_user
    elif command.args is not None:
        if command.args.isdecimal():
            user = await message.chat.get_member(int(command.args))
            user = user.user
        else: return await message.reply('⚠️ <b>Вы ввели неверный ID пользователя!</b>')
    else: user = message.from_user

    member_info = await get_member_chat_info(message.chat.id, user.id)
    if member_info is False: return await message.reply('⚠️ *Пользователя с данным ID не существует!*', parse_mode= "Markdown")
    if member_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    return await message.reply(f'<b>Карточка {hlink(member_info[3], user.url)}</b>\n\n🔑 Уровень - <b>{member_info[9]}</b>. Всего - <b>{member_info[6]} EXP</b>\n🎉 До нового уровня - <b>{member_info[7]} EXP из {member_info[8]} EXP</b>', parse_mode= "HTML")


# /welcome
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('welcome'))
async def get_chat_welcome(message: types.Message):
    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl < 2 or admin_lvl == False: return await message.reply('⚠️ *У вас нет 2-ого и выше уровня доступа!*', parse_mode='Markdown')
    
    welcome = await get_config_data(message.chat.id)
    if welcome is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    return await message.answer(f'👋 Текущее приветствие:\n\n{hcode(welcome[1])}', parse_mode= "HTML")
