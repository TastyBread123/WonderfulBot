from aiogram import Router, types
from aiogram.filters.command import Command

from filters.chat_type import ChatTypeFilter
from database import get_member_chat_info, get_admin_lvl, get_config_data


router = Router()

# /getid
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('getid', 'gid'))
async def get_member_id(message: types.Message):
    if message.reply_to_message is None: return await message.answer('⚠️ *Ответьте на сообщение пользователя чтобы узнать его ID!*', parse_mode='Markdown')

    return await message.answer(f'🔍 ID пользователя @{message.reply_to_message.from_user.username} - <b>{message.reply_to_message.from_user.id}</b>', parse_mode= "HTML")


# /getnick
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("gnick", "getnick"))
async def get_member_nick(message: types.Message):
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы узнать ник отправителя!*', parse_mode='Markdown')
            
    user_data = await get_member_chat_info(message.chat.id, message.reply_to_message.from_user.id)

    if user_data == False: return await message.answer(f'😐 Ник пользователя <b>@{message.reply_to_message.from_user.username} не найден</b>!', parse_mode= "HTML")
    elif user_data is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

    return await message.answer(f'💾 Ник пользователя <b>@{message.reply_to_message.from_user.username}</b> — <b>{user_data[3]}</b>', parse_mode= "HTML")


# /checkvip
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("checkvip"))
async def get_member_vip(message: types.Message):
    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    
    if admin_lvl is None or admin_lvl == False: return None
    if admin_lvl < 1: return await message.reply('⚠️ *У вас нет 1-ого и выше уровня доступа!*', parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ *Ответьте на сообщение, чтобы узнать состояние VIP статуса отправителя!*', parse_mode='Markdown')

    is_vip = await get_member_chat_info(message.chat.id, message.reply_to_message.from_user.id)[5]
    if is_vip is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    if is_vip == 1: return await message.answer(f'😍 У пользователя @{message.reply_to_message.from_user.username} имеется VIP статус')
                
    return await message.answer(f'😔 У пользователя @{message.reply_to_message.from_user.username} отсутствует VIP статус')
    

# /welcome
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('welcome'))
async def get_chat_welcome(message: types.Message):
    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl is False or admin_lvl == False: return None
    if admin_lvl < 2: return await message.reply('⚠️ *У вас нет 2-ого и выше уровня доступа!*', parse_mode='Markdown')
    
    welcome = await get_config_data(message.chat.id)
    if welcome is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

    return await message.answer(f'👋 Текущее приветствие:\n\n<b>{welcome[1]}</b>', parse_mode= "HTML")


# /stats
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('user', 'profile', 'stats'))
async def statistic_member(message: types.Message):
    if message.reply_to_message is None:
        check_info = await get_member_chat_info(message.chat.id, message.from_user.id)
        
        if check_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
        elif check_info == False: return await message.reply('⚠️ Вы не зарегистрированы!*', parse_mode= "Markdown")
        
        vip = 'да' if check_info[5] == 1 else 'нет'
        return await message.reply(f'<b>Профиль пользователя @{check_info[1]} [{check_info[0]}]</b>\n\n💦 Ник пользователя - <b>{check_info[3]}</b>\n👑 VIP: <b>{vip}</b>\n🎓 Количество варнов - <b>{check_info[4]}</b>\n\n🔑 Уровень - <b>{check_info[9]}</b>. Всего - <b>{check_info[6]} EXP</b>\n🎉 До нового уровня - <b>{check_info[7]} EXP из {check_info[8]} EXP</b>', parse_mode= "HTML")
      
    check_info = await get_member_chat_info(message.chat.id, message.reply_to_message.from_user.id)
    if check_info is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    elif check_info == False: return await message.reply('⚠️ Пользователь не зарегистрирован!*', parse_mode= "Markdown")
    
    vip = 'да' if check_info[6] == 1 else 'нет'
    return await message.reply(f'<b>Профиль пользователя @{check_info[1]} [{check_info[0]}]</b>\n\n💦 Ник пользователя - <b>{check_info[3]}</b>\n👑 VIP: <b>{vip}</b>\n🎓 Количество варнов - <b>{check_info[4]}</b>\n\n🔑 Уровень - <b>{check_info[9]}</b>. Всего - <b>{check_info[6]} EXP</b>\n🎉 До нового уровня - <b>{check_info[7]} EXP из {check_info[8]} EXP</b>', parse_mode= "HTML")


# /rank
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('rank'))
async def rank_member(message: types.Message):
    if message.reply_to_message is None:
        check_level = await get_member_chat_info(message.chat.id, message.from_user.id)
        if check_level is False: return await message.reply('⚠️ Вы не зарегистрированы!\n\nРешение: *введите команду /start*', parse_mode= "Markdown")
        if check_level is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
        
        return await message.reply(f'<b>Карточка @{message.from_user.username}</b>\n\n🔑 Уровень - <b>{check_level[9]}</b>. Всего - <b>{check_level[6]} EXP</b>\n🎉 До нового уровня - <b>{check_level[7]} EXP из {check_level[8]} EXP</b>', parse_mode= "HTML")
    
    check_level = await get_member_chat_info(message.chat.id, message.reply_to_message.from_user.id)
    if check_level is False: return await message.reply('⚠️ Вы не зарегистрированы!\n\nРешение: *введите команду /start*', parse_mode= "Markdown")
    if check_level is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
    
    return await message.reply(f'<b>Карточка @{message.reply_to_message.from_user.username}</b>\n\n🔑 Уровень - <b>{check_level[9]}</b>. Всего - <b>{check_level[6]} EXP</b>\n🎉 До нового уровня - <b>{check_level[7]} EXP из {check_level[8]} EXP</b>', parse_mode= "HTML")