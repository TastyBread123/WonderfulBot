from aiogram import Router, types, Bot  
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER

from database import is_user_exists_chat_db, get_config_data, add_user
from filters.chat_type import ChatTypeFilter


router = Router()


@router.chat_member(ChatTypeFilter(chat_type=["group", "supergroup"]), ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member_event(event: types.ChatMemberUpdated, bot: Bot):
    welcome = await get_config_data(event.chat.id)
    if welcome:
        if await is_user_exists_chat_db(event.chat.id, event.new_chat_member.user.id) == False:
            await add_user(event.chat.id, (event.new_chat_member.user.id, event.new_chat_member.user.username, 0, event.new_chat_member.user.first_name, 0, 0, 0, 0, 20, 0))

        return await bot.send_message(event.chat.id, f"@{event.new_chat_member.user.username}\n<b>{welcome[1]}</b>")
