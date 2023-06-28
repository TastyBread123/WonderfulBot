from aiogram import Router, types
from aiogram.filters import Command

from filters.chat_type import ChatTypeFilter
from database import get_admin_lvl


router = Router()

# /pin
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("pin"))
async def pin_mes(message: types.Message):
    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)

    if admin_lvl is False or admin_lvl is None: return None
    if admin_lvl < 2: return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ Ответьте на сообщение, чтобы закрепить его!')

    await message.chat.pin_message(message.reply_to_message.message_id)
    return await message.answer(f'📌 Модератор @{message.from_user.username} <b>закрепил</b> сообщение с ID <b>{message.reply_to_message.message_id}</b>', parse_mode= "HTML")


# /unpin
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("unpin"))
async def unpin_mes(message: types.Message):
    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)

    if admin_lvl is False or admin_lvl is None: return None
    if admin_lvl < 2: return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ Ответьте на сообщение, чтобы открепить его!')

    await message.chat.unpin_message(message.reply_to_message.message_id)
    return await message.answer(f'📌 Модератор @{message.from_user.username} <b>открепил</b> сообщение с ID <b>{message.reply_to_message.message_id}</b>', parse_mode= "HTML")


# /unpinall
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("unpinall"))
async def unpin_all(message: types.Message):
    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    
    if admin_lvl is False or admin_lvl is None: return None
    if admin_lvl < 2: return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
        
    await message.chat.unpin_all_messages()
    return await message.answer(f'📌 Модератор @{message.from_user.username} <b>открепил все закрепленные сообщения</b>', parse_mode= "HTML")