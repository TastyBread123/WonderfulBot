import random
import time
import sqlite3
import datetime
import logging
import os
import asyncio
import aiogram

from aiogram import Dispatcher, executor, types
from aiogram.dispatcher.filters import BoundFilter
from gtts import gTTS

from configs.settings import *
from utils.get_info import get_chat_db_id, is_vip

#Подключение к БД и боту
groups_db = sqlite3.connect('groups.db', check_same_thread=False)
groups_c = groups_db.cursor()
bot = aiogram.Bot(token, parse_mode=None)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


async def get_admin_lvl(message: types.Message):
    try:
        izn_chat_id = str(message.chat.id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0:
                chat_id = chat_id + izn_chat_id[i]

        lvl = groups_c.execute(f"SELECT admin FROM chat_{chat_id} WHERE id = {message.from_user.id}").fetchone()[0]
        return lvl
    except sqlite3.OperationalError:
        await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
        return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        chat_id = get_chat_db_id(message.chat.id)

        try:
            data = groups_c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {message.from_user.id}").fetchone()

            if data is None:
                user_info = (message.from_user.id, message.from_user.username, 0, message.from_user.first_name, 0, 0, 0, 0, 20, 0)
                groups_c.execute(f"INSERT INTO chat_{chat_id}(id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(user_info))
                groups_db.commit()
                return await message.reply("☑️ *Вы успешно зарегистрировались в беседе!*", parse_mode='Markdown')
            else:
                return await message.reply("☑️ *Вы успешно авторизовались в беседе*!", parse_mode='Markdown')

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


class check_admin(BoundFilter):
    key = 'is_admin'
    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin()

dp.filters_factory.bind(check_admin)
@dp.message_handler(commands=["startbot"], is_admin=True)
async def botstart(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            chat_id = get_chat_db_id(message.chat.id)
            data = groups_c.execute(f"SELECT id FROM config WHERE id = {chat_id}").fetchone()
            
            if data is None and (message.chat.type == "group" or "supergroup"):
                start_info = (message.from_user.id, message.from_user.username, 6, message.from_user.first_name, 0, 1, 0, 0, 20, 0)
                config_info = (chat_id, standart_welcome, "Правила еще не установлены!")
                groups_c.execute(f"CREATE TABLE IF NOT EXISTS chat_{chat_id}(id INT, login TEXT, admin INT, nick TEXT, warns INT, vip INT, total_exp INT, tolvl_exp INT, need_exp INT, level INT)")                
                groups_c.execute(f"INSERT INTO chat_{chat_id} (id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (start_info))
                groups_c.execute("INSERT INTO config (id, welcome, rules) VALUES (?, ?, ?)", (config_info))
                groups_db.commit()
                await message.reply("✅ *Бот был успешно запущен в беседе! Вам были выданы права администратора 6 уровня и VIP статус*\n\n*❗️ Напутствие:\nНе забудьте сменить приветствие и правила*!", parse_mode='Markdown')
            
            else:
                await message.reply('❌ Бот *уже* зарегистрирован в чате!', parse_mode='Markdown')
        except:
            await message.answer(f'📄 *Произошла ошибка*\n\nОбратитесь в тех. поддержку для полной информации', parse_mode='Markdown')


@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        return await message.reply('*Команды пользователей*:\n*Основное*:\n/help - список команд\n/start - зарегистрироваться в боте\n/profile(/user) - посмотреть свой профиль (при ответе на сообщение можно посмотреть профиль отправителя)\n/rank - узнать свой уровень и количество EXP(при ответе на сообщение можно посмотреть уровень и EXP отправителя)\n/botinfo - информация о боте\n/rankinfo - информация о системе уровней и EXP\n*Правила* - посмотреть правила\n\n*Развлечения*:\n/mynick *<новый ник>* - изменить себе ник\n/random(/rand) *<от> <до>* - рандомное число\n/chance *<text>* - узнать вероятность того, что указано в text\n/binar *<десятичное число или двоичное число (префикс 0b)>* - перевести десятичное число в двоичное и наоборот\n/say *<текст>* - отправить голосовое сообщение от лица бота\n/write *<текст>* - отправить текстовое сообщение от лица бота\n\n*РП команды*:\n/ebaca(/sex) - трахнуть отправителя\n/kiss - поцеловать отправителя\n/slap - дать подзатыльник отправителю\n/kill - убить отправителя', parse_mode= "Markdown")

@dp.message_handler(commands=['rankinfo'])
async def rankinfo(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        return await message.reply('❗️<b>В боте WonderfulBot есть система уровней!\n\n📌 Изначально у вас 0 уровень и 0 EXP. Чтобы достичь 1 уровня необходимо набрать 20 EXP\nИзначально, за 1 сообщение дается 1 EXP, но создатель может изменить количество до 3 EXP за 1 сообщение.\n\nПосле достижения нового уровня, для получения следующего, вам нужно набрать на 200 EXP больше, чем в прошлый раз.\n\nЧтобы проверить свой уровень и количество EXP - введите команду /rank. Также эта информация содержится в /user(/profile). При ответе на сообщение, с помощью данных команд можно узнать чужой уровень и количество EXP</b>', parse_mode= "HTML")

@dp.message_handler(commands=["botinfo"])
async def botinfo(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        return await message.reply(f'📄 Информация о боте *WonderfulBot*:\n\n💿 *Текущая версия: {version}*\n🤓 *Помощь по командам* - /help\n☕️ *Телеграм канал бота* - [тык]({tg_channel})', parse_mode='Markdown')


@dp.message_handler(content_types=['new_chat_members'])
async def welcome(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        chat_id = get_chat_db_id(message.chat.id)
        
        try:
            data = groups_c.execute(f"SELECT welcome FROM config WHERE id = {chat_id}").fetchone()
            isExistsUser = groups_c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {message.new_chat_members[0].id}").fetchone()
        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
        
        if isExistsUser is None:
            try:
                user_info = (message.new_chat_members[0].id, message.new_chat_members[0].username, 0, message.new_chat_members[0].first_name, 0, 0, 0, 0, 20, 0)
                groups_c.execute(f"INSERT INTO chat_{chat_id}(id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_info))
                groups_db.commit()
                return await message.answer(f'@{message.new_chat_members[0].username}\n{data[0]}')
            except:
                return await message.answer(f'@{message.new_chat_members[0].username}\n{data[0]}')
            
        else:
            try:
                groups_c.execute(f"UPDATE chat_{chat_id} SET admin = 0 WHERE id = ?", (message.new_chat_members[0].id))
                groups_db.commit()
                return await message.answer(f'@{message.new_chat_members[0].username}\n{data[0]}')
            except:
                return await message.answer(f'@{message.new_chat_members[0].username}\n{data[0]}')


@dp.message_handler(commands=["reg"])
async def reg_mem(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        get_admin = await get_admin_lvl(message)
        if get_admin is False:
            return
        if int(get_admin) < 1:
            return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы зарегистрировать отправителя!*', parse_mode='Markdown')
        
        try:
            chat_id = get_chat_db_id(message.chat.id)
            data = groups_c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {message.reply_to_message.from_user.id}").fetchone()
            if data == None:
                user_info = (message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, 0, message.reply_to_message.from_user.first_name, 0, 0, 0, 0, 20, 0)
                groups_c.execute(f"INSERT INTO chat_{chat_id} (id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_info))
                groups_db.commit()

                await message.answer(f'Администратор <b>@{message.from_user.username}</b> зарегистрировал пользователя <b>@{message.reply_to_message.from_user.username}</b>', parse_mode='HTML')
                return await message.delete()
            else:
                return await message.reply('❌ *Пользователь уже зарегистрирован!*', parse_mode='Markdown')
        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")    


@dp.message_handler(commands=['kick'])
async def kick_member(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        get_admin = await get_admin_lvl(message)
        if get_admin is False:
            return
        if int(get_admin) < 1:
            return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
            
        try:
            if message.reply_to_message is None:
                try:
                    kickmem_name = message.get_args().split('@')[1]
                except:
                    return await message.reply("❌ *Вы не упомянули пользователя для кика!*", parse_mode='Markdown')
                
                kickmem_id = groups_c.execute(f"SELECT id FROM chat_{message.chat.id} WHERE login = {kickmem_name}").fetchone()[0]
                        
                await bot.kick_chat_member(message.chat.id, kickmem_id, 30)
                await message.answer(f'😱 Администратор @{message.from_user.username} кикнул пользователя @{kickmem_name}', parse_mode= "HTML")
                return await message.delete()

            else:
                await bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id, 30)
                await message.answer(f'😱 Администратор @{message.from_user.username} кикнул пользователя @{message.reply_to_message.from_user.username}', parse_mode= "HTML")
                return await message.delete()

        except aiogram.utils.exceptions.CantRestrictSelf:
            return await message.reply("❌ *Вы не можете кикнуть меня!*", parse_mode='Markdown')
        except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
            return await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode='Markdown')
        except aiogram.utils.exceptions.CantRestrictChatOwner:
            return await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode='Markdown')



@dp.message_handler(commands=['getid', 'gid'])
async def get_id(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            return await message.answer('⚠️ *Ответьте на сообщение пользователя чтобы узнать его ID!*', parse_mode='Markdown')
        
        await message.answer(f'🔍 ID пользователя @{message.reply_to_message.from_user.username} - <b>{message.reply_to_message.from_user.id}</b>', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=['makeadmin'])
async def set_admin(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        get_admin = await get_admin_lvl(message)
        
        if get_admin is False:
            return
        if get_admin < 5:
            return await message.reply("⚠️ У вас нет 5-ого и выше уровня доступа!", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение пользователя чтобы назначить его на пост администратора!*', parse_mode='Markdown')
            
        try:
            makeadmin_lvl = message.get_args()
            if makeadmin_lvl is None or makeadmin_lvl == ' ' or makeadmin_lvl == '':
                return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */makeadmin <level>*!", parse_mode='Markdown')

            if int(makeadmin_lvl) <= -1:
                return await message.reply("*Нельзя установить -1 и меньше уровень доступа!*", parse_mode='Markdown')
            elif int(makeadmin_lvl) >= 6:
                return await message.reply("*Нельзя установить 6 и больше уровень доступа!*", parse_mode='Markdown')
            
            chat_id = get_chat_db_id(message.chat.id)
            checkadmin = groups_c.execute(f"SELECT admin FROM chat_{chat_id} WHERE id = {message.reply_to_message.from_user.id}").fetchone()

            if checkadmin is not None and int(checkadmin[0]) >= 5:
                return await message.reply("⚠️ *Вы не можете повысить/снять данного пользователя!*", parse_mode='Markdown')

            groups_c.execute(f"UPDATE chat_{chat_id} SET admin=? WHERE id={message.reply_to_message.from_user.id}", (int(makeadmin_lvl),))
            groups_db.commit()

            await message.answer(f'👮 Главный Администратор @{message.from_user.username} назначил пользователя @{message.reply_to_message.from_user.username} <b>администратором {makeadmin_lvl} уровня</b>', parse_mode= "HTML")
            return await message.delete()
            
        except ValueError:
            return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */makeadmin <level>! Аргумент <level> - число*!", parse_mode='Markdown')           


@dp.message_handler(commands=["mute"])
async def mute(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        get_admin = await get_admin_lvl(message)
        if get_admin is False:
            return
        if get_admin < 1:
            return await message.reply("⚠️ У вас нет 1-ого и выше уровня доступа!", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы замутить отправителя!*', parse_mode='Markdown')
        
        try:
            mute_time = message.get_args()
            if mute_time is None or mute_time == ' ' or mute_time == '':
                return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */mute <время в минутах>*!", parse_mode='Markdown')

            new = {'can_send_messages': False, 'can_send_media_messages': False,'can_send_polls': False,'can_send_other_messages': False, 'can_add_web_page_previews': False,}
            await bot.restrict_chat_member(chat_id = message.chat.id, user_id = message.reply_to_message.from_user.id,  permissions= new, until_date=time.time() + int(mute_time)*60)

            if int(mute_time) >= 1:                                                
                await message.answer(f'✅ Администратор @{message.from_user.username} замутил @{message.reply_to_message.from_user.username} на <b>{mute_time} минут</b>', parse_mode= "HTML")
                return await message.delete()
            else:
                await message.answer(f'✅ Администратор @{message.from_user.username} замутил @{message.reply_to_message.from_user.username} <b>навсегда</b>', parse_mode= "HTML")
                return await message.delete()
        
        except aiogram.utils.exceptions.CantRestrictSelf:
            return await message.reply("❌ *Вы не можете замутить меня!*", parse_mode='Markdown')
        except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
            return await message.reply("❌ *Вы не можете замутить данного пользователя!*", parse_mode='Markdown')
        except aiogram.utils.exceptions.CantRestrictChatOwner:
            return await message.reply("❌ *Вы не можете замутить данного пользователя!*", parse_mode='Markdown')   


@dp.message_handler(commands=["unmute"])
async def unmute(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        get_admin = await get_admin_lvl(message)
        if get_admin is False:
            return
        if get_admin < 1:
            return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы размутить отправителя!*', parse_mode='Markdown')
        
        try:
            new = {'can_send_messages': True, 'can_send_media_messages': True,'can_send_polls': True,'can_send_other_messages': True, 'can_add_web_page_previews': True,}
            await bot.restrict_chat_member(chat_id = message.chat.id, user_id = message.reply_to_message.from_user.id, permissions=new)
            await message.answer(f'✅ Администратор @{message.from_user.username} размутил @{message.reply_to_message.from_user.username}', parse_mode= "HTML")
            return await message.delete()

        except aiogram.utils.exceptions.CantRestrictSelf:
            return await message.reply("❌ *Вы не можете размутить меня!*", parse_mode='Markdown')
        except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
            return await message.reply("❌ *Вы не можете размутить данного пользователя!*", parse_mode='Markdown')
        except aiogram.utils.exceptions.CantRestrictChatOwner:
            return await message.reply("❌ *Вы не можете размутить данного пользователя!*", parse_mode='Markdown')            


@dp.message_handler(commands=["ahelp"])
async def ahelp(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 1:
            return await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')
        
        if admin_lvl == 1:
            return await message.reply('Команды *администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute <время в минутах> - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя', parse_mode= "Markdown")
        elif admin_lvl == 2:
            return await message.reply('Команды *администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute *<время в минутах>* - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя\n\n*2-ой уровень*:\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n/unpinall - открепить все сообщения\n/welcome - узнать текущее приветствие\n/clear <кол-во сообщений> - очистить указанное количество сообщений', parse_mode= "Markdown")
        elif admin_lvl == 3:
            return await message.reply('Команды *администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute *<время в минутах>* - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя\n\n*2-ой уровень*:\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n/unpinall - открепить все сообщения\n/welcome - узнать текущее приветствие\n/clear <кол-во сообщений> - очистить указанное количество сообщений\n\n*3-ий уровень*:\n/ban *<время в днях>* - забанить пользователя\n/unban *<id человека, которого нужно разбанить>* - разбанить пользователя\n/warn - выдать варн пользователю\n/unwarn - снять варн пользователю\n/setnick *<новый ник>* - изменить ник пользователю', parse_mode= "Markdown")
        elif admin_lvl == 4:
            return await message.reply('Команды *администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute *<время в минутах>* - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя\n\n*2-ой уровень*:\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n/unpinall - открепить все сообщения\n/welcome - узнать текущее приветствие\n/clear <кол-во сообщений> - очистить указанное количество сообщений\n\n*3-ий уровень*:\n/ban *<время в днях>* - забанить пользователя\n/unban *<id человека, которого нужно разбанить>* - разбанить пользователя\n/warn - выдать варн пользователю\n/unwarn - снять варн пользователю\n/setnick *<новый ник>* - изменить ник пользователю\n\n*4-ый уровень*:\n/title *<новое название>* - изменить название группы\n/description(/desc) *<новое описание>* - изменить описание группы\n/setwelcome *<новое приветствие> - изменить приветствие*', parse_mode= "Markdown")
        elif admin_lvl >= 5:
            return await message.reply('Команды *красной администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute *<время в минутах>* - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя\n\n*2-ой уровень*:\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n/unpinall - открепить все сообщения\n/welcome - узнать текущее приветствие\n/clear <кол-во сообщений> - очистить указанное количество сообщений\n\n*3-ий уровень*:\n/ban *<время в днях>* - забанить пользователя\n/unban *<id человека, которого нужно разбанить>* - разбанить пользователя\n/warn - выдать варн пользователю\n/unwarn - снять варн пользователю\n/setnick *<новый ник>* - изменить ник пользователю\n\n*4-ый уровень*:\n/title *<новое название>* - изменить название группы\n/description(/desc) *<новое описание>* - изменить описание группы\n/setwelcome *<новое приветствие> - изменить приветствие*\n\n*Владелец беседы*:\n/makeadmin *<уровень>* - назначить пользователя на админку\n/setvip *<1 - выдать/2 - забрать>* - выдать или снять VIP статус\n/setrules *<новые правила>* - установить новые правила', parse_mode= "Markdown")


@dp.message_handler(commands=["pin"])
async def pin_mes(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 2:
            return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ Ответьте на сообщение, чтобы закрепить его!')

        await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.answer(f'📌 Администратор @{message.from_user.username} <b>закрепил</b> сообщение с ID <b>{message.reply_to_message.message_id}</b>', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=["unpin"])
async def unpin_mes(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 2:
            return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ Ответьте на сообщение, чтобы открепить его!')

        await bot.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.answer(f'📌 Администратор @{message.from_user.username} <b>открепил</b> сообщение с ID <b>{message.reply_to_message.message_id}</b>', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=["unpinall"])
async def unpin_all(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 2:
            return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
        
        await bot.unpin_all_chat_messages(message.chat.id)
        await message.answer(f'📌 Администратор @{message.from_user.username} <b>открепил все закрепленные сообщения</b>', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=["title"])
async def set_title(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 4:
            return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
        
        new_title = message.get_args()
        if new_title is None or new_title == ' ' or new_title == '':
            return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */title <новое название>*!", parse_mode='Markdown')
                
        await bot.set_chat_title(message.chat.id, new_title)
        await message.answer(f'🍩 Администратор @{message.from_user.username} изменил название беседы на <b>{new_title}</b>', parse_mode= "HTML")
        return await message.delete()



@dp.message_handler(commands=["ban"])
async def ban_mem(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 3:
            return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            await message.reply('⚠️ *Ответьте на сообщение, чтобы забанить отправителя!*', parse_mode= "Markdown")
            
        else:
            until_date = message.get_args()
            if until_date is None or until_date == ' ' or until_date == '':
                return await message.reply("⚠️ Неверный синтаксис!\nИспользуйте: */ban <срок в днях>*!", parse_mode='Markdown')
                            
            try:
                isvip = groups_c.execute(f"SELECT vip FROM chat_{get_chat_db_id(message.chat.id)} WHERE id = {message.reply_to_message.from_user.id}").fetchone()[0]
                if int(isvip) == 1 and int(until_date) > 10:
                    return await message.reply('⚠️ Вы не можете забанить человека с VIP статусом более чем на 10 дней!')
            except TypeError:
                pass
            
            try:
                await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id, until_date=time.time() + int(until_date)*86400)
            except aiogram.utils.exceptions.CantRestrictSelf:
                return await message.reply("❌ *Вы не можете забанить меня!*", parse_mode= "Markdown")
            except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
                return await message.reply("❌ *Вы не можете забанить данного пользователя!*", parse_mode= "Markdown")
            except aiogram.utils.exceptions.CantRestrictChatOwner:
                return await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode= "Markdown")
                
            if int(until_date) >= 1:
                await message.answer(f'✅ Администратор @{message.from_user.username} забанил пользователя @{message.reply_to_message.from_user.username} на <b>{until_date} дней</b>', parse_mode= "HTML")                
                return await message.delete()
            else:
                await message.answer(f'✅ Администратор @{message.from_user.username} забанил пользователя @{message.reply_to_message.from_user.username} <b>навсегда</b>', parse_mode= "HTML")
                return await message.delete()


@dp.message_handler(commands=["warn"])
async def warn_mem(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 3:
            return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы заварнить отправителя!*', parse_mode= "Markdown")

        chat_id = get_chat_db_id(message.chat.id)

        data = groups_c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {message.reply_to_message.from_user.id}").fetchone()
        if data == None:
            return await message.reply('❌ *Пользователь не зарегистрирован. Зарегистрируйте его с помощью команды /reg*', parse_mode= "Markdown")

        groups_c.execute(f"UPDATE chat_{chat_id} SET warns = warns + {1} WHERE id= ?", (message.reply_to_message.from_user.id,))
        groups_db.commit()
        warns_total = groups_c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()[0]
        await message.answer(f'✅ Администратор @{message.from_user.username} <b>выдал предупреждение</b> пользователю @{message.reply_to_message.from_user.username}\nТекущее количество - {warns_total}', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=["unwarn"])
async def unwarn_mem(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 3:
            return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы разварнить отправителя!*', parse_mode= "Markdown")
        
        chat_id = get_chat_db_id(message.chat.id)
        total_warns = groups_c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()[0]
                
        if total_warns is None or total_warns <= 0:
            return await message.reply('⛔️ *У пользователя нет предупреждений!*', parse_mode='Markdown')
                
        groups_c.execute(f"UPDATE chat_{chat_id} SET warns = warns - {1} WHERE id = ?", (message.reply_to_message.from_user.id,))
        groups_db.commit()
        total_warns = groups_c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()[0]

        await message.answer(f'✅ Администратор @{message.from_user.username} снял предупреждение пользователю @{message.reply_to_message.from_user.username}\nУ пользователя осталось <b>{total_warns} предупреждений</b>', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=["user", "profile", "stats"])
async def check_stat(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        chat_id = get_chat_db_id(message.chat.id)
        if message.reply_to_message is None:
            try:
                check_info = groups_c.execute(f"SELECT nick, warns, level, total_exp, tolvl_exp, need_exp, vip FROM chat_{chat_id} WHERE id = {message.from_user.id}").fetchone()
                if check_info is None:
                    return await message.reply('⚠️ Вы не зарегистрированы!\n\nРешение: *введите команду /start*', parse_mode= "Markdown")
                return await message.reply(f'<b>Профиль пользователя @{message.from_user.username}</b>\n\n💦 Ник пользователя - <b>{check_info[0]}</b>\n👑 VIP: <b>{is_vip(state=check_info[6])}</b>\n🎓 Количество варнов - <b>{check_info[1]}</b>\n\n🔑 Уровень - <b>{check_info[2]}</b>. Всего - <b>{check_info[3]} EXP</b>\n🎉 До нового уровня - <b>{check_info[4]} EXP из {check_info[5]} EXP</b>', parse_mode= "HTML")
            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        else:
            try:
                check_info = groups_c.execute(f"SELECT nick, warns, level, total_exp, tolvl_exp, need_exp, vip FROM chat_{chat_id} WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()
                if check_info is None:
                    return await message.reply('⚠️ Пользователь не зарегистрирован!\n\nРешение: *введите команду /start*', parse_mode= "Markdown")
                return await message.reply(f'<b>Профиль пользователя @{message.reply_to_message.from_user.username}</b>\n\n💦 Ник пользователя - <b>{check_info[0]}</b>\n👑 VIP: <b>{is_vip(state=check_info[6])}</b>\n🎓 Количество варнов - <b>{check_info[1]}</b>\n\n🔑 Уровень - <b>{check_info[2]}</b>. Всего - <b>{check_info[3]} EXP</b>\n🎉 До нового уровня - <b>{check_info[4]} EXP из {check_info[5]} EXP</b>', parse_mode= "HTML")
            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")



@dp.message_handler(commands=["rank"])
async def set_nick(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        chat_id = get_chat_db_id(message.chat.id)

        if message.reply_to_message is None:
            try:
                check_level = groups_c.execute(f"SELECT level, total_exp, tolvl_exp, need_exp FROM chat_{chat_id} WHERE id = ?", (message.from_user.id,)).fetchone()
                if check_level is None:
                    return await message.reply('⚠️ Вы не зарегистрированы!\n\nРешение: *введите команду /start*', parse_mode= "Markdown")
                return await message.reply(f'<b>Карточка @{message.from_user.username}</b>\n\n🔑 Уровень - <b>{check_level[0]}</b>. Всего - <b>{check_level[1]} EXP</b>\n🎉 До нового уровня - <b>{check_level[2]} EXP из {check_level[3]} EXP</b>', parse_mode= "HTML")
            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        else:
            try:
                check_level = groups_c.execute(f"SELECT level, total_exp, tolvl_exp, need_exp FROM chat_{chat_id} WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()
                if check_level is None:
                    return await message.reply('⚠️ Пользователь не зарегистрирован!\n\nРешение: *введите команду /start*', parse_mode= "Markdown")
                return await message.reply(f'<b>Карточка @{message.reply_to_message.from_user.username}</b>\n\n🔑 Уровень - <b>{check_level[0]}</b>. Всего - <b>{check_level[1]} EXP</b>\n🎉 До нового уровня - <b>{check_level[2]} EXP из {check_level[3]} EXP</b>', parse_mode= "HTML")

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


@dp.message_handler(commands=["mynick"])
async def mynick(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            chat_id = get_chat_db_id(message.chat.id)
            new_nick = message.get_args()
            if new_nick is None or new_nick == ' ' or new_nick == '':
                return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */mynick <новый ник>*!', parse_mode='Markdown')
                
            groups_c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = ?", (message.from_user.id,))
            groups_c.execute(f"UPDATE chat_{chat_id} SET nick = ? WHERE id= ?", (new_nick, message.from_user.id))
            groups_db.commit()
            
            await message.answer(f'💡 Пользователь @{message.from_user.username} изменил свой ник на <b>{new_nick}</b>', parse_mode= "HTML")
            return await message.delete()            
        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


@dp.message_handler(commands=["setnick", "snick"])
async def set_another_nick(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 3:
            return await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы изменить ник отправителя!*', parse_mode= "Markdown")
        try:
            new_nick = message.get_args()
            if new_nick is None or new_nick == ' ' or new_nick == '':
                return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */setnick <новый ник>*!', parse_mode='Markdown')
            
            groups_c.execute(f"UPDATE chat_{get_chat_db_id(message.chat.id)} SET nick = ? WHERE id= ?", (new_nick, message.reply_to_message.from_user.id))
            groups_db.commit()

            await message.answer(f'💡 Администратор <b>@{message.from_user.username}</b> изменил ник <b>@{message.reply_to_message.from_user.username}</b> на <b>{new_nick}</b>', parse_mode= "HTML")
            return await message.delete()

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


@dp.message_handler(commands=["gnick", "getnick"])
async def get_another_nick(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы узнать ник отправителя!*', parse_mode='Markdown')
            
        chat_id = get_chat_db_id(message.chat.id)

        try:
            check_nick = groups_c.execute(f"SELECT nick FROM chat_{chat_id} WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()[0]
        except TypeError:
            await message.answer(f'😐 Ник пользователя <b>@{message.reply_to_message.from_user.username} не найден</b>!', parse_mode= "HTML")
            return await message.delete()
        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        await message.answer(f'💾 Ник пользователя <b>@{message.reply_to_message.from_user.username}</b> — <b>{check_nick}</b>', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=["clear"])
async def clear_chat(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 2:
            return await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')
        try:
            clear = int(message.get_args())
            if clear is None or clear == ' ' or clear == '':
                return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */clear <кол-во сообщений>*!', parse_mode='Markdown')
        except ValueError:
            return await message.reply("⚠️ *Количество сообщений должно быть числом!*", parse_mode='Markdown')
        
        message_id = message.message_id
        i = 0
        exceptions = 0
        while i < int(clear):
            if exceptions >= 50:
                await message.answer(f'😢 Слишком много удаленных сообщений в чате!\nБыло очищено только <b>{i}</b> из <b>{clear}</b> сообщений', parse_mode= "HTML")
                break

            try:
                message_id -= 1
                await bot.delete_message(message.chat.id, message_id)
                i += 1
            except aiogram.utils.exceptions.MessageCantBeDeleted:
                await message.answer(f'✅ Было удалено только <b>{i}</b> из <b>{clear}</b> сообщений из-за <b>ограничений Telegram</b>!', parse_mode= "HTML")
                break
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                exceptions += 1 
        else:
            return await message.answer(f'✅ Были очищены все <b>{i}</b> из <b>{clear}</b> сообщений!', parse_mode= "HTML")


@dp.message_handler(commands=["rand", "random"])
async def random_chisl(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            from_num, to_num = message.get_args().split(' ', maxsplit=1)

            resul_rand = random.randint(int(from_num), int(to_num))
            await message.answer(f'🎲 @{message.from_user.username}, ваше рандомное число от <b>{from_num}</b> до <b>{to_num}</b> — <b>{resul_rand}</b>', parse_mode= "HTML")
            return await message.delete()

        except IndexError:
            return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */rand <от> <до>**", parse_mode='Markdown')

        except ValueError:
            return await message.reply("⚠️ Ошибка радиуса или в аргументах используется текст!\n\nИспользуйте: */rand <ОТ> <ДО>*", parse_mode='Markdown')



@dp.message_handler(commands=["desc", "description"])
async def set_desc(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 4:
            return await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')
        
        new_title = message.get_args()
        if new_title is None or new_title == ' ' or new_title == '':
            return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */description <new description>*!", parse_mode='Markdown')

        await bot.set_chat_description(message.chat.id, new_title)
        await message.answer(f'😱 Администратор <b>@{message.from_user.username}</b> изменил описание беседы на <b>{new_title}</b>', parse_mode= "HTML")
        await message.delete()


@dp.message_handler(commands=["sex", "ebaca"])
async def sex_ebaca(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            who = message.get_args()
            if who is None:
                return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */sex @username*', parse_mode='Markdown')

            photo = open(f'{dir}/data/imgs/ebat.jpg', 'rb')
            await message.answer_photo(photo, f'👉👈 Пупсик @{message.from_user.username} трахнул секс-машину {who}')
            return await message.delete()
            
        else:
            try:
                photo = open(f'{dir}/data/imgs/ebat.jpg', 'rb')
                await message.answer_photo(photo, f'👉👈 Пупсик @{message.from_user.username} трахнул секс-машину @{message.reply_to_message.from_user.username}')
                return await message.delete()
            except:
                return await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["kiss"])
async def kiss(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            who = message.get_args()
            if who is None:
                return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */kiss @username*', parse_mode='Markdown')

            photo = open(f'{dir}/data/imgs/kiss.png', 'rb')
            await message.answer_photo(photo, f'😍 Малыш @{message.from_user.username} поцеловал зайчика {who}')
            return await message.delete()
            
        else:
            try:
                photo = open(f'{dir}/data/imgs/kiss.png', 'rb')
                await message.answer_photo(photo, f'😍 Малыш @{message.from_user.username} поцеловал зайчика @{message.reply_to_message.from_user.username}')
                return await message.delete()
            except:
                return await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["kill"])
async def kill(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            who = message.get_args()
            if who is None:
                return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */kill @username*', parse_mode='Markdown')

            photo = open(f'{dir}//data//imgs/kill.png', 'rb')
            await message.answer_photo(photo, f'🔪 Маньяк @{message.from_user.username} хладнокровно убил беднягу {who}')
            return await message.delete()
            
        else:
            try:
                photo = open(f'{dir}//data//imgs/kill.png', 'rb')
                await message.answer_photo(photo, f'🔪 Маньяк @{message.from_user.username} хладнокровно убил беднягу @{message.reply_to_message.from_user.username}')
                return await message.delete()
            except:
                return await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["slap"])
async def slap(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            who = message.get_args()
            if who is None:
                return await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */slap @username*', parse_mode='Markdown')

            photo = open(f'{dir}imgs/slap.jpg', 'rb')
            await message.answer_photo(photo, f'😤 Буллер @{message.from_user.username} дал подзатыльник {who}')
            return await message.delete()
            
        else:
            try:
                photo = open(f'{dir}imgs/slap.jpg', 'rb')
                await message.answer_photo(photo, f'😤 Буллер @{message.from_user.username} дал подзатыльник @{message.reply_to_message.from_user.username}')
                return await message.delete()
            except:
                return await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["setvip"])
async def set_vip(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 5:
            return await message.reply('⚠️ *У вас нет 5-ого и выше уровня доступа!*', parse_mode='Markdown')
        
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы выдать или снять VIP статус отправителю!*', parse_mode='Markdown')
        
        chat_id = get_chat_db_id(message.chat.id)
        give_vip = message.get_args()
        if give_vip is None or give_vip == ' ' or give_vip == '':
                return await message.reply('⚠️ Неверный синтаксис!\n\n*/setvip <1 - выдать/2 - забрать>*', parse_mode='Markdown')

        if give_vip == '0':
                groups_c.execute(f"UPDATE chat_{chat_id} SET vip = '0' WHERE id= ?", (message.reply_to_message.from_user.id,))
                groups_db.commit()

                await message.answer(f'💎 Администратор @{message.from_user.username} снял <b>VIP статус</b> пользователю @{message.reply_to_message.from_user.username}', parse_mode= "HTML")
                return await message.delete()
        elif give_vip == '1':
                groups_c.execute(f"UPDATE chat_{chat_id} SET vip = '1' WHERE id= ?", (message.reply_to_message.from_user.id,))
                groups_db.commit()
                        
                await message.answer(f'💎 Администратор @{message.from_user.username} выдал <b>VIP статус</b> пользователю @{message.reply_to_message.from_user.username}', parse_mode= "HTML")
                return await message.delete()
        else:
            return await message.reply('⚠️ *Неверный аргумент! 1 - выдать/2 - забрать!*', parse_mode='Markdown')            


@dp.message_handler(commands=["checkvip"])
async def check_vip(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 5:
            return await message.reply('⚠️ *У вас нет 5-ого и выше уровня доступа!*', parse_mode='Markdown')
        
        if message.reply_to_message is None:
            return await message.reply('⚠️ *Ответьте на сообщение, чтобы узнать состояние VIP статуса отправителя!*', parse_mode='Markdown')

        chat_id = get_chat_db_id(message.chat.id)
        nick_check = groups_c.execute(f"SELECT vip FROM chat_{chat_id} WHERE id = ?", (message.reply_to_message.from_user.id,)).fetchone()[0]

        if int(nick_check) == 1:
            await message.answer(f'😍 У пользователя @{message.reply_to_message.from_user.username} имеется VIP статус')
            return await message.delete()
                
        elif int(nick_check) == 0:
            await message.answer(f'😔 У пользователя @{message.reply_to_message.from_user.username} отсутствует VIP статус')
            return await message.delete()
        

@dp.message_handler(commands=["unban"])
async def unban_mem(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 3:
            return await message.reply('⚠️ *У вас нет 5-ого и выше уровня доступа!*', parse_mode='Markdown')

        unbanmember_id = message.get_args()
        if unbanmember_id is None or unbanmember_id == ' ' or unbanmember_id == '':
            return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */unban <user id>*", parse_mode='Markdown')

        await bot.unban_chat_member(message.chat.id, unbanmember_id)
        await message.answer(f'🥰 Администратор @{message.from_user.username} разбанил пользователя с ID <b>{unbanmember_id}</b>', parse_mode= "HTML")
        return await message.delete()


@dp.message_handler(commands=['chance'])
async def chance(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        resul_rand = random.randint(0, 100)
        reson = message.get_args()
        if reson is None or reson == ' ' or reson == '':
            return await message.reply("⚠️ Неверный синтаксис!\n\n/chance *<текст>*", parse_mode='Markdown')

        if resul_rand >=90:
            await message.answer(f'🙀 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=80 and resul_rand <=89:
            await message.answer(f'😀 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=70 and resul_rand <=79:
            await message.answer(f'😄 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=60 and resul_rand <=69:
            await message.answer(f'😅 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=50 and resul_rand <=59:
            await message.answer(f'😌 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=40 and resul_rand <=49:
            await message.answer(f'😒 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=30 and resul_rand <=39:
            await message.answer(f'😔 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=20 and resul_rand <=29:
            await message.answer(f'😫 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()
        elif resul_rand >=10 and resul_rand <=19:
            await message.answer(f'😢 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()  
        elif resul_rand <=9:
            await message.answer(f'😭 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
            return await message.delete()


@dp.message_handler(commands=['welcome'])
async def get_welcome(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 2:
            return await message.reply('⚠️ *У вас нет 2-ого и выше уровня доступа!*', parse_mode='Markdown')
            
        chat_id = get_chat_db_id(message.chat.id)
        welcome = groups_c.execute(f"SELECT welcome FROM config WHERE id = {chat_id}").fetchone()[0]
        if welcome is None:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        await message.answer(f'👋 Текущее приветствие - <b>{welcome}</b>', parse_mode= "HTML")
        return await message.delete()

@dp.message_handler(commands=['setwelcome'])
async def setwelcome(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 4:
            return await message.reply('⚠️ *У вас нет 4-ого и выше уровня доступа!*', parse_mode='Markdown')
        try:
            chat_id = get_chat_db_id(message.chat.id)
            old_welcome = groups_c.execute(f"SELECT welcome FROM config WHERE id = {chat_id}").fetchone()[0]

            new_welcome = message.get_args()
            if new_welcome is None or new_welcome == ' ' or new_welcome == '':
                return await message.reply("⚠️ Неверный синтаксис!\n\n/setwelcome *<новое приветствие>*", parse_mode='Markdown')

            groups_c.execute(f"UPDATE config SET welcome = ? WHERE id = {chat_id}", (new_welcome,))
            groups_db.commit()
            await message.answer(f'😒 Старое приветствие - <b>{old_welcome}</b>\n😃 Новое приветствие - <b>{new_welcome}</b>\n\n😇 Изменил @{message.from_user.username}', parse_mode= "HTML")
            return await message.delete()

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


@dp.message_handler(commands=['setrules'])
async def setrules(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        admin_lvl = await get_admin_lvl(message)
        if admin_lvl is False:
            return
        if admin_lvl < 5:
            return await message.reply('⚠️ *У вас нет 5-ого и выше уровня доступа!*', parse_mode='Markdown')
        try:
            chat_id = get_chat_db_id(message.chat.id)
            old_rules = groups_c.execute(f"SELECT rules FROM config WHERE id = {chat_id}").fetchone()[0]

            new_rules = message.text.split(maxsplit=1)[1]
            if new_rules is None or new_rules == ' ' or new_rules == '':
                return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */setrules <новые правила>*", parse_mode='Markdown')
                
            groups_c.execute(f"UPDATE config SET rules = ? WHERE id = {chat_id}", (new_rules,))
            groups_db.commit()
            await message.answer(f'😒 Старые правила - <b>{old_rules}</b>\n😃 Новые правила - <b>{new_rules}</b>\n\n😇 Изменил @{message.from_user.username}', parse_mode= "HTML")
            return await message.delete()

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


#Перевод в бинарное число
@dp.message_handler(commands=['binar'])
async def binar(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            number = message.get_args()
            if number is None or number == ' ' or number == '':
                return await message.reply('⚠️ <b>Неверный синтаксис!</b>\n\nИспользуйте: <b>/binar (для перевода в двоичное введите любое десятичное число (Пример: 654). Для перевода в десятиченое перед двоичным числом поставьте префикс 0b) </b>', parse_mode= "HTML")
            
            if number.startswith('0b'):
                res = int(number, 2)
                return await message.reply(f'🤩 Перевод двоичного числа в десятичное:\n\n<b>🧐 Запрос (двоичное): {number}</b>\n\n<b>📌 Перевод (десятичное): {res}</b>', parse_mode= "HTML")
            else:
                return await message.reply(f'🤩 Перевод десятичного числа в двоичное:\n\n<b>🧐 Запрос (десятичное): {number}</b>\n\n<b>📌 Перевод (двоичное): {int(number):0{9 if int(number) > 0 else 10}b}</b>', parse_mode= "HTML")
        
        except ValueError:
            return await message.reply('⚠️ <b>Ошибка чисел</b>\n\nИспользуйте: /binar <b>(ЧИСЛО/ЧИСЛО с префиксом 0b)</b>', parse_mode= "HTML")


#Анонимное сообщение
@dp.message_handler(commands=['write'])
async def bot_write_cmd(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        say = message.get_args()
        if say is None or say == ' ' or say == '':
            return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */write <текст>*', parse_mode='Markdown')            

        if len(say) <= 256:
            try:
                await message.delete()
                await message.answer(f'🤨 <i>Анонимное сообщение</i>:\n\n<b>{say}</b>', parse_mode= "HTML")
            except:
                await message.reply('⚠️ *Произошла ошибка. Попробуйте позже*', parse_mode='Markdown')
                return message.delete()
        else:
            await message.reply('⚠️ Нельзя использовать *более 256 символов*!', parse_mode='Markdown')
            return message.delete()


#Голосовое сообщение от бота, GTTS
@dp.message_handler(commands=['say'])
async def bot_say_cmd(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        say = message.get_args()
        if say is None or say == ' ' or say == '':
            return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */say <текст>*', parse_mode='Markdown')
    
        if len(say) <= 128:
            try: 
                var = gTTS(text = say, lang = 'ru')
                var.save(f'temp_data\\{message.from_user.id}.mp3')
                var = open(f'temp_data\\{message.from_user.id}.mp3', 'rb')
            except:
                await message.reply('⚠️ *Произошла ошибка. Попробуйте позже*', parse_mode='Markdown')
                try:
                    return os.remove(f'temp_data\\{message.from_user.id}.mp3')
                except:
                    pass
            
            try:
                await message.answer_audio(var)
                return os.remove(f'temp_data\\{message.from_user.id}.mp3')
            except:
                pass

        else:
            return await message.reply('⚠️ Нельзя использовать *более 128 символов*!', parse_mode='Markdown')

@dp.message_handler(text = ['Правила', 'правила'])
async def every_message(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            chat_id = get_chat_db_id(message.chat.id)

            rules = groups_c.execute(f"SELECT rules FROM config WHERE id = {chat_id}").fetchone()[0]
            return await message.reply(f'<b>{rules}</b>', parse_mode= "HTML")
        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode='Markdown')


@dp.message_handler()
async def every_message(message: types.Message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            chat_id = get_chat_db_id(message.chat.id)

            groups_c.execute(f"UPDATE chat_{chat_id} SET total_exp = total_exp + {1}, tolvl_exp = tolvl_exp + {1}  WHERE id= ?", (message.from_user.id,))
            groups_db.commit()
            await asyncio.sleep(1)
            messages_check = groups_c.execute(f"SELECT tolvl_exp, need_exp FROM chat_{chat_id} WHERE id = {message.from_user.id}").fetchone()
            
            if messages_check[0] >= messages_check[1]:
                groups_c.execute(f"UPDATE chat_{chat_id} SET level = level + {1}, tolvl_exp = {0}, need_exp = need_exp + {100} WHERE id= ?", (message.from_user.id,))
                groups_db.commit()
                level_check = groups_c.execute(f"SELECT level FROM chat_{chat_id} WHERE id = {message.from_user.id}").fetchone()[0]

                return await message.reply(f'<b>Вы успешно повысили свой уровень!\nТекущий уровень - {level_check}\n\nПродолжайте общаться в том же духе 💖</b>', parse_mode= "HTML") 
        except:
            pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=print(f"{datetime.datetime.now()} | Бот v. {version} успешно запущен!"))