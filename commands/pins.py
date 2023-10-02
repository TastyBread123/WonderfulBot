from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.utils.markdown import hcode, hlink

from filters.chat_type import ChatTypeFilter
from database import get_member_chat_info


router = Router()

# /pin
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("pin"))
async def pin_mes(message: types.Message):
    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info[2] < 2 or admin_info is False or admin_info is None: return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ Ответьте на сообщение, чтобы закрепить его!')

    await message.chat.pin_message(message.reply_to_message.message_id)
    return await message.answer(f'📌 Модератор {hlink(admin_info[3], message.from_user.url)} <b>закрепил</b> сообщение с ID <b>{hlink(str(message.reply_to_message.message_id), message.reply_to_message.get_url())}</b>', parse_mode= "HTML")


# /unpin
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("unpin"))
async def unpin_mes(message: types.Message):
    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info[2] < 2 or admin_info is False or admin_info is None: return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
    if message.reply_to_message is None: return await message.reply('⚠️ Ответьте на сообщение, чтобы открепить его!')

    await message.chat.unpin_message(message.reply_to_message.message_id)
    return await message.answer(f'📌 Модератор {hlink(admin_info[3], message.from_user.url)} <b>открепил</b> сообщение с ID <b>{hlink(str(message.reply_to_message.message_id), message.reply_to_message.get_url())}</b>', parse_mode= "HTML")


# /unpinall
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("unpinall"))
async def unpin_all(message: types.Message):
    admin_info = await get_member_chat_info(message.chat.id, message.from_user.id)
    if admin_info[2] < 2 or admin_info is False or admin_info is None: return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
        
    await message.chat.unpin_all_messages()
    return await message.answer(f'📌 Модератор {hlink(admin_info[3], message.from_user.url)} <b>открепил все закрепленные сообщения</b>', parse_mode= "HTML")