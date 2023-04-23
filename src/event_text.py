from aiogram.filters import Text
from aiogram import Router, types, F
from filters.chat_type import ChatTypeFilter

from database import get_config_data, add_message_chat_user, add_user


router = Router()

@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Text('правила', ignore_case=True))
async def rules_message_handler(message: types.Message):
    welcome = get_config_data(message.chat.id)
    if welcome is None: return await message.reply('👋 Создатель беседы еще не зарегистрировал бота и не добавил правила')

    return await message.answer(f'👋 Правила беседы:\n\n<b>{welcome[0]}</b>', parse_mode= "HTML")


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), F.text)
async def every_message(message: types.Message):
    level = add_message_chat_user(message.chat.id, message.from_user.id)
    if level == 'UserError':
        return add_user(message.chat.id, (message.from_user.id, message.from_user.username, 0, message.from_user.first_name, 0, 0, 0, 0, 20, 0))
    
    if type(level) is int: return await message.answer(f'@{message.from_user.username}\n<b>Вы успешно повысили свой уровень!\nТекущий уровень - {level}\n\nПродолжайте общаться в том же духе 💖</b>', parse_mode= "HTML") 
        
