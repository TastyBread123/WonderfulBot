from aiogram import Router, types
from aiogram.filters.command import Command

from filters.chat_type import ChatTypeFilter
from configs.settings import version, tg_channel
from configs.commands import admin_cmds_1lvl, admin_cmds_2lvl, admin_cmds_3lvl, admin_cmds_4lvl, admin_cmds_5lvl
from database import get_admin_lvl


router = Router()

# /help
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("help"))
async def help(message: types.Message):
    return await message.reply('*Команды пользователей*:\n*Основное*:\n/help - список команд\n/start - зарегистрироваться в боте\n/profile(/user) - посмотреть свой профиль (при ответе на сообщение можно посмотреть профиль отправителя)\n/getid(/gid) - узнать ID отправителя\n/getnick(/gnick) - узнать ник отправителя\n/rank - узнать свой уровень и количество EXP(при ответе на сообщение можно посмотреть уровень и EXP отправителя)\n/botinfo - информация о боте\n/rankinfo - информация о системе уровней и EXP\n*Правила* - посмотреть правила\n\n*Развлечения*:\n/mynick *<новый ник>* - изменить себе ник\n/random(/rand) *<от> <до>* - рандомное число\n/chance *<text>* - узнать вероятность того, что указано в text\n/binar *<десятичное число или двоичное число (префикс 0b)>* - перевести десятичное число в двоичное и наоборот\n/say *<текст>* - отправить голосовое сообщение от лица бота\n/write *<текст>* - отправить текстовое сообщение от лица бота\n\n*РП команды*:\n/sex - изнасиловать отправителя\n/kiss - поцеловать отправителя\n/slap - дать подзатыльник отправителю\n/kill - убить отправителя', parse_mode= "Markdown")


# /rankinfo
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('rankinfo'))
async def rankinfo(message: types.Message):
    return await message.reply('❗️<b>В боте WonderfulBot есть система уровней!\n\n📌 Изначально у вас 0 уровень и 0 EXP. Чтобы достичь 1 уровня необходимо набрать 20 EXP\nИзначально, за 1 сообщение дается 1 EXP, но создатель может изменить количество до 3 EXP за 1 сообщение.\n\nПосле достижения нового уровня, для получения следующего, вам нужно набрать на 200 EXP больше, чем в прошлый раз.\n\nЧтобы проверить свой уровень и количество EXP - введите команду /rank. Также эта информация содержится в /user(/profile). При ответе на сообщение, с помощью данных команд можно узнать чужой уровень и количество EXP</b>', parse_mode= "HTML")


# /botinfo
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("botinfo"))
async def botinfo(message: types.Message):
    return await message.reply(f'📄 Информация о боте *WonderfulBot*:\n\n💿 *Текущая версия: {version}*\n🤓 *Помощь по командам* - /help\n☕️ *Телеграм канал бота* - [тык]({tg_channel})', parse_mode='Markdown')


# /ahelp
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command("ahelp"))
async def ahelp(message: types.Message):
    admin_lvl = await get_admin_lvl(message.chat.id, message.from_user.id)
    if admin_lvl == False or admin_lvl is None: return None
    if admin_lvl < 1: return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')

    text1 = ''
    for i in admin_cmds_1lvl: text1+=f'{i} {admin_cmds_1lvl[i]}\n'
    text2 = ''
    for i in admin_cmds_2lvl: text2+=f'{i} {admin_cmds_2lvl[i]}\n'
    text3 = ''
    for i in admin_cmds_3lvl: text3+=f'{i} {admin_cmds_3lvl[i]}\n'
    text4 = ''
    for i in admin_cmds_4lvl: text4+=f'{i} {admin_cmds_4lvl[i]}\n'
    text5 = ''
    for i in admin_cmds_5lvl: text5+=f'{i} {admin_cmds_5lvl[i]}\n'
        
    return await message.reply(f'1 уровень:\n{text1}\n2 уровень:\n{text2}\n3 уровень:\n{text3}\n4 уровень:\n{text4}\n5 уровень:\n{text5}', parse_mode='Markdown')

