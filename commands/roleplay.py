from aiogram import Router, types
from aiogram.utils.markdown import hlink
from aiogram.filters.command import Command, CommandObject

from filters.chat_type import ChatTypeFilter

router = Router()

@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("sex"))
async def sex_ebaca(message: types.Message, command: CommandObject):
    if message.reply_to_message is None:
        who = command.args
        if who is None: return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */sex @username*', parse_mode='Markdown')
        return await message.answer(f'👉👈 Пупсик @{message.from_user.username} изнасиловал секс-машину {who}')
    
    return await message.answer(f'👉👈 Пупсик @{message.from_user.username} изнасиловал секс-машину @{message.reply_to_message.from_user.username}')


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("kiss"))
async def kiss(message: types.Message, command: CommandObject):
    if message.reply_to_message is None:
        who = command.args
        if who is None: return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */kiss @username*', parse_mode='Markdown')
        return await message.answer(f'😍 Малыш @{message.from_user.username} поцеловал зайчика {who}')
            
    return await message.answer(f'😍 Малыш @{message.from_user.username} поцеловал зайчика @{message.reply_to_message.from_user.username}')            


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("kill"))
async def kill(message: types.Message, command: CommandObject):
    if message.reply_to_message is None:
        who = command.args
        if who is None: return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */kill @username*', parse_mode='Markdown')
        return await message.answer(f'🔪 Маньяк @{message.from_user.username} хладнокровно убил беднягу {who}')
            
    return await message.answer(f'🔪 Маньяк @{message.from_user.username} хладнокровно убил беднягу @{message.reply_to_message.from_user.username}')


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("slap"))
async def slap(message: types.Message, command: CommandObject):
    if message.reply_to_message is None:
        who = command.args
        if who is None: return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */slap @username*', parse_mode='Markdown')
        return await message.answer(f'😤 Буллер @{message.from_user.username} дал подзатыльник {who}')
            
    return await message.answer(f'😤 Буллер @{message.from_user.username} дал подзатыльник @{message.reply_to_message.from_user.username}')
