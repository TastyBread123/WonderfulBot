import random
import time
import sqlite3
import datetime
import logging
import os
import asyncio
import aiogram
import magic_filter


from aiogram import Dispatcher, executor
from aiogram.dispatcher.filters import BoundFilter
from PIL import Image
from gtts import gTTS

from config import token, dir, version

#Подключение к БД и боту
db = sqlite3.connect('C:\\!python\\проекты\\bot_chat\\Bot System\\bot.db', check_same_thread=False)
c = db.cursor()
bot = aiogram.Bot(token, parse_mode=None)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


#Вывод в консоль об успешном запуске
date = datetime.datetime.now()
print(f"{date} | Бот v. {version} успешно запущен!")

@dp.message_handler(commands=['start'])
async def start(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]
        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            data = c.fetchone()

            if data is None:
                adminn = 0
                nickn = "Не установлен"
                warnss = 0
                vipp = 0
                user_name = message.from_user.username
                total_exp = 0
                tolvl_exp = 0
                need_exp = 20
                level = 0

                user_info = (int(user_id), str(user_name), int(adminn), str(nickn), int(warnss), int(vipp), int(total_exp), int(tolvl_exp), int(need_exp), int(level))
                c.execute(f"INSERT INTO chat_{chat_id}(id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(user_info))
                db.commit()
                await message.reply("☑️ *Вы успешно зарегистрировались в боте!*", parse_mode='Markdown')

            else:
                await message.reply("☑️ *Вы успешно авторизовались*!", parse_mode='Markdown')

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
async def botstart(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            res_chat_id = ""
            chat_id = message.chat.id
            chat_id=str(chat_id)

            for i in range(0, len(chat_id)): 
                if i != 0: 
                    res_chat_id = res_chat_id + chat_id[i]

            c.execute(f"SELECT id FROM config WHERE id = {res_chat_id}")
            data = c.fetchone()
            
            if data is None and (message.chat.type == "group" or "supergroup"):
                starter_id = message.from_user.id
                standart_welcome = "Приветствуем в беседе!"
                user_name = message.from_user.username

                start_info = (starter_id, str(user_name), 6, 'Не установлен', 0, 1, 0, 0, 20, 0)
                config_info = (res_chat_id, standart_welcome, "Правила еще не установлены!")
                
                c.execute(f"""CREATE TABLE IF NOT EXISTS chat_{res_chat_id}(
                id INT,
                login TEXT,
                admin INT,
                nick TEXT,
                warns INT,
                vip INT,
                total_exp INT,
                tolvl_exp INT,
                need_exp INT,
                level INT)
                """)
                db.commit()
                

                c.execute(f"INSERT INTO chat_{res_chat_id} (id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (start_info))
                db.commit()
                c.execute("INSERT INTO config (id, welcome, rules) VALUES (?, ?, ?)", (config_info))
                db.commit()

                await message.reply("✅ *Бот был успешно запущен в беседе! Вам были выданы права администратора 6 уровня и VIP статус*\n\n*❗️ Напутствие:\nНе забудьте сменить приветствие и правила*!", parse_mode='Markdown')
            
            else:
                await message.reply('❌ Бот *уже* зарегистрирован в чате!', parse_mode='Markdown')
        
        except:
            await message.answer(f'📄 *Произошла ошибка*\n\nОбратитесь в тех. поддержку для полной информации', parse_mode='Markdown')



@dp.message_handler(commands=["help"])
async def help(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        return await message.reply('*Команды пользователей*:\n*Основное*:\n/help - список команд\n/start - зарегистрироваться в боте\n/profile(/user) - посмотреть свой профиль (при ответе на сообщение можно посмотреть профиль отправителя)\n/rank - узнать свой уровень и количество EXP(при ответе на сообщение можно посмотреть уровень и EXP отправителя)\n/botinfo - информация о боте\n/rankinfo - информация о системе уровней и EXP\nПравила - посмотреть правила\n\n*Развлечения*:\n/mynick *<новый ник>* - изменить себе ник\n/random(/rand) *<от> <до>* - рандомное число\n/chance *<text>* - узнать вероятность того, что указано в text\n/binar *<десятичное число или двоичное число (префикс 0b)>* - перевести десятичное число в двоичное и наоборот\n/say *<текст>* - отправить голосовое сообщение от лица бота\n/write *<текст>* - отправить текстовое сообщение от лица бота\n\n*РП команды*:\n/ebaca(/sex) - трахнуть отправителя\n/kiss - поцеловать отправителя\n/slap - дать подзатыльник отправителю\n/kill - убить отправителя', parse_mode= "Markdown")


@dp.message_handler(commands=["botinfo"])
async def botinfo(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        return await message.reply(f'📄 Информация о боте *WonderfulBot*:\n\n💿 *Версия: {version}*\n🤓 *Помощь по командам* - /help\n🖥 *Проверка состояния бота* - [тык](https://stats.uptimerobot.com/4PGZDSzK4B/792996254)\n\n☕️ *Телеграм канал бота* - [тык](https://t.me/wonderful_bot_channel)', parse_mode='Markdown')


@dp.message_handler(content_types=['new_chat_members'])
async def welcome(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        user_name = message.new_chat_members[0].username

        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            data = c.fetchone()

            chat_id = message.chat.id
            chat_id=str(chat_id)

            res_chat_id = ''
            for i in range(0, len(chat_id)): 
                if i != 0: 
                    res_chat_id = res_chat_id + chat_id[i]

            c.execute(f"SELECT welcome FROM config WHERE id = {res_chat_id}")
            welcome = c.fetchone()[0]
        
        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
        
        if data is None:
            try:
                adminn = 0
                nickn = "Не установлен"
                warnss = 0
                vipp = 0
                level = 0
                user_name = message.from_user.username
                total_exp = 0
                tolvl_exp = 0
                need_exp = 50

                user_info = (int(user_id), str(user_name), int(adminn), str(nickn), int(warnss), int(vipp), int(total_exp), int(tolvl_exp), int(need_exp), int(level))
                c.execute(f"INSERT INTO chat_{chat_id}(id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(user_info))
                db.commit()

                await message.answer(f'@{user_name}\n{welcome}')

            except:
                try:
                    await message.answer(f'@{user_name}\n{welcome}')

                except sqlite3.OperationalError:
                    return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")
            
        else:
            try:
                admin = 0
                c.execute("UPDATE users SET admin = ? WHERE id = ?", (admin, int(user_id)))
                db.commit()

                await message.answer(f'@{user_name}\n{welcome}')
            
            except:
                try:
                    await message.answer(f'@{user_name}\n{welcome}')

                except sqlite3.OperationalError:
                    return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


@dp.message_handler(commands=["reg"])
async def reg_mem(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 1:
            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы зарегистрировать отправителя!*', parse_mode='Markdown')
            
            else:
                try:
                    warnmem_id = message.reply_to_message.from_user.id
                    warnmember_name = message.reply_to_message.from_user.username
                    user_name = message.from_user.username

                    c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {warnmem_id}")
                    data = c.fetchone()

                    if data == None:
                        adminn = 0
                        nickn = "Не установлен"
                        warnss = 1
                        vipp = 0
                        level = 0
                        total_exp = 0
                        tolvl_exp = 0
                        need_exp = 20

                        user_info = (int(warnmem_id), str(warnmember_name), int(adminn), str(nickn), int(warnss), int(vipp), int(total_exp), int(tolvl_exp), int(need_exp), int(level))
                        c.execute(f"INSERT INTO chat_{chat_id} (id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_info))
                        db.commit()

                        await message.answer(f'Администратор <b>@{user_name}</b> зарегистрировал пользователя <b>@{warnmember_name}<*b>', parse_mode='HTML')
                        await message.delete()

                    else:
                        await message.reply('❌ *Пользователь уже зарегистрирован!*', parse_mode='Markdown')

                except sqlite3.OperationalError:
                    return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        else:
            await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=['kick'])
async def kick_member(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 1:
            try:
                if message.reply_to_message is None:
                    try:
                        kickmem_name = message.text.split('@', maxsplit=1)[1]

                        c.execute(f"SELECT id FROM chat_{chat_id} WHERE login = {kickmem_name}")
                        kickmem_id = c.fetchone()[0]
                        
                        await bot.kick_chat_member(chat_id, kickmem_id, 30)
                        await message.answer(f'😱 Администратор @{adminmem} кикнул пользователя @{kickmem_name}', parse_mode= "HTML")
                        await message.delete()

                        date = datetime.datetime.now()
                        print(f'{date} | Администратор {adminmem} кикнул пользователя {kickmem_name}')

                    except:
                        print("Произошла ошибка!")
                
                else:
                    chat_id = message.chat.id
                    adminmem = message.from_user.username
                    kickmem_id = message.reply_to_message.from_user.id
                    kickmem_name = message.reply_to_message.from_user.username

                    await bot.kick_chat_member(chat_id, kickmem_id, 30)
                    await message.answer(f'😱 Администратор @{adminmem} кикнул пользователя @{kickmem_name}', parse_mode= "HTML")
                    await message.delete()

                    date = datetime.datetime.now()
                    print(f'{date} | Администратор {adminmem} кикнул пользователя {kickmem_name}')

            except aiogram.utils.exceptions.CantRestrictSelf:
                    await message.reply("❌ *Вы не можете кикнуть меня!*", parse_mode='Markdown')

            except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
                    await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode='Markdown')

            except aiogram.utils.exceptions.CantRestrictChatOwner:
                await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode='Markdown')

        else:
            await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')



@dp.message_handler(commands=['getid', 'gid'])
async def get_id(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 1:
            if message.reply_to_message is None:
                await message.answer('⚠️ *Ответьте на сообщение пользователя чтобы узнать его ID!*', parse_mode='Markdown')
        
            else:
                getkmem_id = message.reply_to_message.from_user.id
                getmem_name = message.reply_to_message.from_user.username
                await message.answer(f'🔍 ID пользователя @{getmem_name} - <b>{getkmem_id}</b>', parse_mode= "HTML")
                await message.delete()

        else:
            await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=['makeadmin'])
async def set_admin(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        whoisset = message.from_user.id

        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {whoisset}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 5:
            whoisset_name = message.from_user.username

            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение пользователя чтобы назначить его на пост администратора!*', parse_mode='Markdown')
            
            else:
                try:
                    setadmin_id = message.reply_to_message.from_user.id
                    setadmin_name = message.reply_to_message.from_user.username

                    makeadmin_lvl = message.text.split(maxsplit=1)[1]
                    makeadmin_info = (makeadmin_lvl)

                    if int(makeadmin_lvl) <= -1:
                        await message.reply("*Нельзя установить -1 и меньше уровень доступа!*", parse_mode='Markdown')

                    elif int(makeadmin_lvl) >= 6:
                        await message.reply("*Нельзя установить 6 и больше уровень доступа!*", parse_mode='Markdown')

                    else:
                        c.execute(f"SELECT admin FROM chat_{chat_id} WHERE id = {setadmin_id}")
                        checkadmin = c.fetchone()[0]

                        if int(checkadmin) >= 6:
                            await message.reply("⚠️ *Вы не можете повысить/снять данного пользователя!*", parse_mode='Markdown')
                            
                        else:
                            c.execute(f"UPDATE chat_{chat_id} SET admin=? WHERE id={setadmin_id}", (makeadmin_info))
                            db.commit()

                            await message.answer(f'👮 Главный Администратор @{whoisset_name} назначил пользователя @{setadmin_name} <b>администратором {makeadmin_lvl} уровня</b>', parse_mode= "HTML")
                            await message.delete()

                            date = datetime.datetime.now()
                            print(f'{date} | Главный Администратор {whoisset_name} назначил пользователя {setadmin_name} администратором {makeadmin_lvl} уровня')

                except IndexError:
                    await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */makeadmin <level>*!", parse_mode='Markdown')

                except ValueError:
                    await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */makeadmin <level>! Аргумент <level> - число*!", parse_mode='Markdown')

        else:
            await message.reply("⚠️ У вас нет 5-ого и выше уровня доступа!", parse_mode='Markdown')


@dp.message_handler(commands=["mute"])
async def mute(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        whoismute = message.from_user.id

        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {whoismute}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 1:
            whoismute_name = message.from_user.username

            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы замутить отправителя!*', parse_mode='Markdown')
            
            else:
                try:
                    mute_time = message.text.split(maxsplit=1)[1]

                    new = {'can_send_messages': False, 'can_send_media_messages': False,'can_send_polls': False,'can_send_other_messages': False, 'can_add_web_page_previews': False,}

                    await bot.restrict_chat_member(chat_id = message.chat.id, user_id = message.reply_to_message.from_user.id,  permissions= new, until_date=time.time() + int(mute_time)*60)

                    if int(mute_time) >= 1:
                        punishman_name = message.reply_to_message.from_user.username
                        
                        date = datetime.datetime.now()
                        print(f'{date} | Администратор {whoismute_name} замутил пользователя {punishman_name} на {mute_time} минут')
                        
                        await message.answer(f'✅ Администратор @{whoismute_name} замутил @{punishman_name} на <b>{mute_time} минут</b>', parse_mode= "HTML")
                        await message.delete()

                    else:
                        punishman_name = message.reply_to_message.from_user.username
                        
                        date = datetime.datetime.now()
                        print(f'{date} | Администратор {whoismute_name} замутил пользователя {punishman_name} навсегда')
                        
                        await message.answer(f'✅ Администратор @{whoismute_name} замутил @{punishman_name} <b>навсегда</b>', parse_mode= "HTML")
                
                except IndexError:
                    await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: /mute <время(в минутах)>!", parse_mode='Markdown')

                except aiogram.utils.exceptions.CantRestrictSelf:
                    await message.reply("❌ *Вы не можете замутить меня!*", parse_mode='Markdown')

                except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
                    await message.reply("❌ *Вы не можете замутить данного пользователя!*", parse_mode='Markdown')

                except aiogram.utils.exceptions.CantRestrictChatOwner:
                    await message.reply("❌ *Вы не можете замутить данного пользователя!*", parse_mode='Markdown')

        else:
            await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["unmute"])
async def unmute(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        whoismute = message.from_user.id

        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {whoismute}")
            isadmin = c.fetchone()

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin[0] >= 1:
            whoismute_name = message.from_user.username

            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы размутить отправителя!*', parse_mode='Markdown')
            
            else:
                try:
                    punishman_name = message.reply_to_message.from_user.username
                    new = {'can_send_messages': True, 'can_send_media_messages': True,'can_send_polls': True,'can_send_other_messages': True, 'can_add_web_page_previews': True,}

                    await bot.restrict_chat_member(chat_id = message.chat.id, user_id = message.reply_to_message.from_user.id, permissions=new)

                except aiogram.utils.exceptions.CantRestrictSelf:
                    await message.reply("❌ *Вы не можете размутить меня!*", parse_mode='Markdown')

                except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
                    await message.reply("❌ *Вы не можете размутить данного пользователя!*", parse_mode='Markdown')

                except aiogram.utils.exceptions.CantRestrictChatOwner:
                    await message.reply("❌ *Вы не можете размутить данного пользователя!*", parse_mode='Markdown')

                
                date = datetime.datetime.now()
                print(f'{date} | Администратор {whoismute_name} размутил пользователя {punishman_name}')

                await message.answer(f'✅ Администратор @{whoismute_name} размутил @{punishman_name}', parse_mode= "HTML")
                await message.delete()
        
        else:
            await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["ahelp"])
async def ahelp(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode='Markdown')

        if isadmin == 1:
            await message.reply('Команды *администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute <время в минутах> - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя', parse_mode= "Markdown")
        
        elif isadmin == 2:
            await message.reply('Команды *администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute *<время в минутах>* - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя\n\n*2-ой уровень*:\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n/unpinall - открепить все сообщения\n/welcome - узнать текущее приветствие', parse_mode= "Markdown")
        
        elif isadmin == 3:
            await message.reply('Команды *администрации*:', parse_mode= "Markdown")
        
        elif isadmin == 4:
            await message.reply('Команды *администрации*:', parse_mode= "Markdown")

        elif isadmin >= 5:
            await message.reply('Команды *администрации*:' + '\n\n*1-ый уровень*:\n/ahelp - показать список команд\n/kick - кикнуть пользователя\n/mute *<время в минутах>* - замутить пользователя\n/unmute - снять мут пользователю\n/getid(/gid) - узнать ID пользователя\n/getnick(/gnick) - узнать ник пользователя\n/checkvip - проверить наличие VIP статуса\n/reg - зарегистрировать пользователя\n\n*2-ой уровень*:\n/pin - закрепить сообщение\n/unpin - открепить сообщение\n/unpinall - открепить все сообщения\n/welcome - узнать текущее приветствие\n\n*3-ий уровень*:\n/ban *<время в днях>* - забанить пользователя\n/unban *<id человека, которого нужно разбанить>* - разбанить пользователя\n/warn - выдать варн пользователю\n/unwarn - снять варн пользователю\n/setnick *<новый ник>* - изменить ник пользователю\n\n*4-ый уровень*:\n/title *<новое название>* - изменить название группы\n/description(/desc) *<новое описание>* - изменить описание группы\n/setwelcome *<новое приветствие> - изменить приветствие*\n\n*Владелец беседы*:\n/makeadmin *<уровень>* - назначить пользователя на админку\n/setvip *<1 - выдать/2 - забрать>* - выдать или снять VIP статус\n/setrules *<новые правила>* - установить новые правила', parse_mode= "Markdown")

        else:
            await message.reply("⚠️ *У вас нет 1-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["pin"])
async def pin_mes(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 2:
            if message.reply_to_message is None:
                await message.reply('⚠️ Ответьте на сообщение, чтобы закрепить его!')
            
            else:
                user_name = message.from_user.username
                pin_name = message.reply_to_message.message_id
                chat_id = message.chat.id

                await bot.pin_chat_message(chat_id, pin_name)

                date = datetime.datetime.now()
                print(f'{date} | Администратор {user_name} закрепил сообщение с ID {pin_name}')
                
                await message.answer(f'📌 Администратор @{user_name} <b>закрепил</b> сообщение с ID <b>{pin_name}</b>', parse_mode= "HTML")
                await message.delete()
        
        else:
            await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["unpin"])
async def unpin_mes(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 2:
            if message.reply_to_message is None:
                await message.reply('⚠️ Ответьте на сообщение, чтобы открепить его!')
            
            else:
                user_name = message.from_user.username
                unpin_name = message.reply_to_message.message_id
                chat_id = message.chat.id

                await bot.unpin_chat_message(chat_id, unpin_name)

                date = datetime.datetime.now()
                print(f'{date} | Администратор {user_name} открепил сообщение с ID {unpin_name}')

                await message.answer(f'📌 Администратор @{user_name} <b>открепил</b> сообщение с ID <b>{unpin_name}</b>', parse_mode= "HTML")
                await message.delete()
        
        else:
            await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["unpinall"])
async def unpin_all(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 2:
            user_name = message.from_user.username
            chat_id = message.chat.id

            await bot.unpin_all_chat_messages(chat_id)

            date = datetime.datetime.now()
            print(f'{date} | Администратор {user_name} открепил все сообщения беседы')

            await message.answer(f'📌 Администратор @{user_name} <b>открепил все закрепленные сообщения</b>', parse_mode= "HTML")
            await message.delete()
        
        else:
            await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["title"])
async def set_title(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 4:
            try:
                chat_id = message.chat.id
                user_name = message.from_user.username
                new_title = message.text.split(maxsplit=1)[1]
                
                await bot.set_chat_title(chat_id, new_title)
                await message.answer(f'🍩 Администратор @{user_name} изменил название беседы на <b>{new_title}</b>', parse_mode= "HTML")
                await message.delete()

                date = datetime.datetime.now()
                print(f'{date} | Администратор {user_name} изменил название беседы на {new_title}')

            except IndexError:
                await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */title <новое название>*!", parse_mode= "Markdown")

        else:
            await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode= "Markdown")


@dp.message_handler(commands=["ban"])
async def ban_mem(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 3:

            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы забанить отправителя!*', parse_mode= "Markdown")
            
            else:
                try:
                    banmember_id = message.reply_to_message.from_user.id
                    banmember_name = message.reply_to_message.from_user.username
                    user_name = message.from_user.username
                    until_date = message.text.split(maxsplit=1)[1]
                    
                    c.execute(f"SELECT vip FROM chat_{chat_id} WHERE id = {banmember_id}")
                    isvip = c.fetchone()[0]
                    
                    if int(isvip) == 1:
                        if int(until_date) > 10:
                            await message.reply('⚠️ Вы не можете забанить человека с VIP статусом более чем на 10 дней!')
                        
                        else:
                            await bot.ban_chat_member(chat_id, banmember_id, until_date=time.time() + int(until_date)*86400)
                        
                            if int(until_date) >= 1:
                                await message.answer(f'✅ Администратор @{user_name} забанил пользователя @{banmember_name} на <b>{until_date} дней</b>', parse_mode= "HTML")
                                await message.delete()

                            else:
                                await message.answer(f'✅ Администратор @{user_name} забанил пользователя @{banmember_name} <b>навсегда</b>', parse_mode= "HTML")
                                await message.delete()
                    
                    else:
                        bot.ban_chat_member(chat_id, banmember_id, until_date=time.time() + int(until_date)*86400)
                        
                        if int(until_date) >= 1:
                            await message.answer(f'✅ Администратор @{user_name} забанил пользователя @{banmember_name} на <b>{until_date} дней</b>', parse_mode= "HTML")                
                            await message.delete()

                        else:
                            await message.answer(f'✅ Администратор @{user_name} забанил пользователя @{banmember_name} <b>навсегда</b>', parse_mode= "HTML")
                            await message.delete()

                except IndexError:
                    await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */ban <срок (в днях)>*!", parse_mode= "Markdown")

                except aiogram.utils.exceptions.CantRestrictSelf:
                    await message.reply("❌ *Вы не можете забанить меня!*", parse_mode= "Markdown")
                
                except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
                    await message.reply("❌ *Вы не можете забанить данного пользователя!*", parse_mode= "Markdown")

                except aiogram.utils.exceptions.CantRestrictChatOwner:
                    await message.reply("❌ *Вы не можете кикнуть данного пользователя!*", parse_mode= "Markdown")
        
        else:
            await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["warn"])
async def warn_mem(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 3:
            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы заварнить отправителя!*', parse_mode= "Markdown")
            
            else:
                warnmem_id = message.reply_to_message.from_user.id
                warnmember_name = message.reply_to_message.from_user.username
                user_name = message.from_user.username

                c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {warnmem_id}")
                data = c.fetchone()

                if data == None:
                    await message.reply('❌ *Пользователь не зарегистрирован. Зарегистрируйте его с помощью команды /reg*', parse_mode= "Markdown")

                else:
                    plus = 1
                    c.execute(f"UPDATE chat_{chat_id} SET warns = warns + ? WHERE id= ?", (plus, warnmem_id))
                    db.commit()

                    c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = {warnmem_id}")
                    skolko = c.fetchone()[0]
                    
                    await message.answer(f'✅ Администратор @{user_name} <b>выдал предупреждение</b> пользователю @{warnmember_name}\nТекущее количество - {skolko}', parse_mode= "HTML")
                    await message.delete()

        else:
            await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["unwarn"])
async def unwarn_mem(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0:
                chat_id = chat_id + izn_chat_id[i]
        
        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 3:
            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы снят предупреждение отправителю!*', parse_mode='Markdown')
            
            else:
                warnmem_id = message.reply_to_message.from_user.id
                warnmember_name = message.reply_to_message.from_user.username
                user_name = message.from_user.username

                c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {warnmem_id}")
                data = c.fetchone()

                if data == None:
                    await message.reply('⛔️ *У пользователя нет предупреждений!*', parse_mode='Markdown')

                else:
                    c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = {warnmem_id}")
                    skolko = c.fetchone()[0]
                
                    if skolko <= 0:
                        await message.reply('⛔️ *У пользователя нет предупреждений!*', parse_mode='Markdown')
                
                    else:
                        minus = 1
                        c.execute(f"UPDATE chat_{chat_id} SET warns = warns - ? WHERE id = ?", (minus, warnmem_id))
                        db.commit()

                        c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = {warnmem_id}")
                        skolko = c.fetchone()[0]

                        await message.answer(f'✅ Администратор @{user_name} снял предупреждение пользователю @{warnmember_name}\nУ пользователя осталось <b>{skolko} предупреждений</b>', parse_mode= "HTML")
                        await message.delete()

        else:
            await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["user", "profile"])
async def check_stat(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        user_id = message.from_user.id
        user_name = message.from_user.username

        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        if message.reply_to_message is None:
            try:
                c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = {user_id}")
                check_warns = c.fetchone()[0]
                c.execute(f"SELECT nick FROM chat_{chat_id} WHERE id = {user_id}")
                check_nick = c.fetchone()[0]
                c.execute(f"SELECT level FROM chat_{chat_id} WHERE id = {user_id}")
                check_level = c.fetchone()[0]
                c.execute(f"SELECT total_exp FROM chat_{chat_id} WHERE id = {user_id}")
                check_totalexp = c.fetchone()[0]
                c.execute(f"SELECT tolvl_exp FROM chat_{chat_id} WHERE id = {user_id}")
                check_tolvlexp = c.fetchone()[0]
                c.execute(f"SELECT need_exp FROM chat_{chat_id} WHERE id = {user_id}")
                check_needexp = c.fetchone()[0]

                await message.reply(f'<b>Профиль пользователя @{user_name}</b>\n\n💦 Ник пользователя - <b>{check_nick}</b>\n🎓 Количество варнов - <b>{check_warns}</b>\n\n🔑 Уровень - <b>{check_level}</b>. Всего - <b>{check_totalexp} EXP</b>\n🎉 До нового уровня - <b>{check_tolvlexp} EXP из {check_needexp} EXP</b>', parse_mode= "HTML")

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

            
        
        else:
            checkmem_id = message.reply_to_message.from_user.id
            checkmember_name = message.reply_to_message.from_user.username
            try:
                c.execute(f"SELECT warns FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_warns = c.fetchone()[0]
                c.execute(f"SELECT nick FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_nick = c.fetchone()[0]
                c.execute(f"SELECT level FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_level = c.fetchone()[0]
                c.execute(f"SELECT total_exp FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_totalexp = c.fetchone()[0]
                c.execute(f"SELECT tolvl_exp FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_tolvlexp = c.fetchone()[0]
                c.execute(f"SELECT need_exp FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_needexp = c.fetchone()[0]

                await message.reply(f'<b>Профиль пользователя @{checkmember_name}</b>\n\n💦 Ник пользователя - <b>{check_nick}</b>\n🎓 Количество варнов - <b>{check_warns}</b>\n\n🔑 Уровень - <b>{check_level}</b>. Всего - <b>{check_totalexp} EXP</b>\n🎉 До нового уровня - <b>{check_tolvlexp} EXP из {check_needexp} EXP</b>', parse_mode= "HTML")

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")



@dp.message_handler(commands=["rank"])
async def set_nick(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0: 
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            user_name = message.from_user.username

            try:
                c.execute(f"SELECT level FROM chat_{chat_id} WHERE id = {user_id}")
                check_level = c.fetchone()[0]
                c.execute(f"SELECT total_exp FROM chat_{chat_id} WHERE id = {user_id}")
                check_totalexp = c.fetchone()[0]
                c.execute(f"SELECT tolvl_exp FROM chat_{chat_id} WHERE id = {user_id}")
                check_tolvlexp = c.fetchone()[0]
                c.execute(f"SELECT need_exp FROM chat_{chat_id} WHERE id = {user_id}")
                check_needexp = c.fetchone()[0]

                await message.reply(f'<b>Карточка @{user_name}</b>\n\n🔑 Уровень - <b>{check_level}</b>. Всего - <b>{check_totalexp} EXP</b>\n🎉 До нового уровня - <b>{check_tolvlexp} EXP из {check_needexp} EXP</b>', parse_mode= "HTML")

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        else:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0: 
                    chat_id = chat_id + izn_chat_id[i]

            checkmem_id = message.reply_to_message.from_user.id
            checkmember_name = message.reply_to_message.from_user.username

            try:
                c.execute(f"SELECT level FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_level = c.fetchone()[0]
                c.execute(f"SELECT total_exp FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_totalexp = c.fetchone()[0]
                c.execute(f"SELECT tolvl_exp FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_tolvlexp = c.fetchone()[0]
                c.execute(f"SELECT need_exp FROM chat_{chat_id} WHERE id = {checkmem_id}")
                check_needexp = c.fetchone()[0]

                await message.reply(f'<b>Карточка @{checkmember_name}</b>\n\n🔑 Уровень - <b>{check_level}</b>. Всего - <b>{check_totalexp} EXP</b>\n🎉 До нового уровня - <b>{check_tolvlexp} EXP из {check_needexp} EXP</b>', parse_mode= "HTML")

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


@dp.message_handler(commands=["mynick"])
async def mynick(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0: 
                    chat_id = chat_id + izn_chat_id[i]
            
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            user_name = message.from_user.username
            new_nick = message.text.split(maxsplit=1)[1]

            

            c.execute(f"UPDATE chat_{user_id} SET nick = ? WHERE id= ?", (new_nick, user_id))
            db.commit()
            
            await message.answer(f'💡 Пользователь @{user_name} изменил свой ник на <b>{new_nick}</b>', parse_mode= "HTML")
            await message.delete()

        except IndexError:
            await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */mynick <новый ник>*!', parse_mode='Markdown')

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")


@dp.message_handler(commands=["setnick", "snick"])
async def set_another_nick(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        user_id = message.from_user.id
        user_name = message.from_user.username
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 3:
            try:
                if message.reply_to_message is None:
                    await message.reply('⚠️ *Ответьте на сообщение, чтобы изменить ник отправителя!*', parse_mode='Markdown')
                
                else:
                    new_nick = message.text.split(maxsplit=1)[1]
                    change_id = message.reply_to_message.from_user.id
                    change_name = message.reply_to_message.from_user.username

                    c.execute(f"UPDATE chat_{chat_id} SET nick = ? WHERE id= ?", (new_nick, change_id))
                    db.commit()

                    await message.answer(f'💡 Администратор <b>@{user_name}</b> изменил ник <b>@{change_name}</b> на <b>{new_nick}</b>', parse_mode= "HTML")
                    await message.delete()

            except IndexError:
                await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */setnick <новый ник>*!", parse_mode='Markdown')

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        else:
            await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["gnick", "getnick"])
async def get_another_nick(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]
        
        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 1:
            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы узнать ник отправителя!*', parse_mode='Markdown')
            
            else:
                change_id = message.reply_to_message.from_user.id
                change_name = message.reply_to_message.from_user.username

                try:
                    c.execute(f"SELECT nick FROM chat_{chat_id} WHERE id = {change_id}")
                    check_nick = c.fetchone()[0]

                except TypeError:
                    await message.answer(f'😐 Ник пользователя <b>@{change_name} не найден</b>!', parse_mode= "HTML")
                    return await message.delete()

                await message.answer(f'💾 Ник пользователя <b>@{change_name}</b> — <b>{check_nick}</b>', parse_mode= "HTML")
                return await message.delete()
                    
                    
        else:
            return message.reply("⚠️ У вас нет 1-ого и выше уровня доступа!")


@dp.message_handler(commands=["clear"])
async def clear_chat(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0:
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 2:
            try:
                clear = message.text.split(maxsplit=1)[1]
            except IndexError:
                clear = 10

            message_id = message.message_id
            i = 0
            exceptions = 0
        
            while i < int(clear):
                if exceptions >= 50:
                    await message.answer(f'😢 Слишком много удаленных сообщений в чате!\nБыло очищено только <b>{i}</b> из <b>{clear}</b> сообщений', parse_mode= "HTML")
                    break

                message_id -= 1
                i += 1

                try:
                    await bot.delete_message(message.chat.id, message_id)

                except aiogram.utils.exceptions.MessageCantBeDeleted:
                    await message.answer(f'✅ Было удалено только <b>{i}</b> из <b>{clear}</b> сообщений из-за <b>ограничений Telegram</b>!', parse_mode= "HTML")
                    break

                except aiogram.utils.exceptions.MessageToDeleteNotFound:
                    i -= 1
                    exceptions += 1 
            else:
                await message.answer(f'✅ Были очищены все <b>{i}</b> из <b>{clear}</b> сообщений!', parse_mode= "HTML")

        else:
            await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["rand", "random"])
async def random_chisl(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            user_name = message.from_user.username

            ot = message.text.split(maxsplit=2)[1]
            do = message.text.split(maxsplit=2)[2]

            resul_rand = random.randint(int(ot), int(do))

            await message.answer(f'🎲 @{user_name}, ваше рандомное число от <b>{ot}</b> до <b>{do}</b> — <b>{resul_rand}</b>', parse_mode= "HTML")
            return await message.delete()

        except IndexError:
            return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */rand <от> <до>**", parse_mode='Markdown')

        except ValueError:
            return await message.reply("⚠️ Ошибка радиуса или в аргументах используется текст!\n\nИспользуйте: */rand <ОТ> <ДО>*", parse_mode='Markdown')



@dp.message_handler(commands=["desc", "description"])
async def set_desc(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /reg*', parse_mode='Markdown')

        if isadmin >= 4:
            try:
                chat_id = message.chat.id
                user_name = message.from_user.username
                new_title = message.text.split(maxsplit=1)[1]

                await bot.set_chat_description(chat_id, new_title)
                
                await message.answer(f'😱 Администратор <b>@{user_name}</b> изменил описание беседы на <b>{new_title}</b>', parse_mode= "HTML")
                await message.delete()

                date = datetime.datetime.now()
                print(f'{date} | Администратор {user_name} изменил описание беседы на {new_title}')

            except IndexError:
                await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */description <new description>*!", parse_mode='Markdown')

        else:
            await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=["sex", "ebaca"])
async def sex_ebaca(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            try:
                user_name = message.from_user.username
                who = message.text.split('@', maxsplit=1)[1]

                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/ebat.jpg', 'rb')
                await message.answer_photo(photo, f'👉👈 Пупсик @{user_name} трахнул секс-машину @{who}')
                await message.delete()

            except IndexError:
                await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */sex @username*', parse_mode='Markdown')

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Пользователь отсутствует в базе данных!\n\nРешение: *введите команду /reg*', parse_mode='Markdown')

            
        else:
            try:
                user_name = message.from_user.username
                change_name = message.reply_to_message.from_user.username

                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/ebat.jpg', 'rb')
                await message.answer_photo(photo, f'👉👈 Пупсик @{user_name} трахнул секс-машину @{change_name}')
                await message.delete()

            except:
                await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["kiss"])
async def kiss(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            try:
                user_name = message.from_user.username
                who = message.text.split('@', maxsplit=1)[1]
                
                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/kiss.png', 'rb')
                await message.answer_photo(photo, f'😍 Малыш @{user_name} поцеловал зайчика @{who}')
                await message.delete()

            except IndexError:
                await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */kiss @username*', parse_mode='Markdown')

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Пользователь отсутствует в базе данных!\n\nРешение: *введите команду /reg*', parse_mode='Markdown')
            
        else:
            try:
                user_name = message.from_user.username
                change_name = message.reply_to_message.from_user.username

                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/kiss.png', 'rb')
                await message.answer_photo(photo, f'😍 Малыш @{user_name} поцеловал зайчика @{change_name}')
                await message.delete()

            except:
                await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["kill"])
async def kill(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            try:
                user_name = message.from_user.username
                who = message.text.split('@', maxsplit=1)[1]

                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/kill.png', 'rb')
                await message.answer_photo(photo, f'🔪 Маньяк @{user_name} хладнокровно убил беднягу @{who}')
                await message.delete()

            except IndexError:
                await message.reply('⚠️ Неверный синтаксис.\n\nИспользуйте: */kill @username*', parse_mode='Markdown')

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Пользователь отсутствует в базе данных!\n\nРешение: *введите команду /reg*', parse_mode='Markdown')
            
        else:
            try:
                user_name = message.from_user.username
                change_name = message.reply_to_message.from_user.username

                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/kill.png', 'rb')
                await message.answer_photo(photo, f'🔪 Маньяк @{user_name} хладнокровно убил беднягу @{change_name}')
                await message.delete()
            
            except:
                await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["slap"])
async def slap(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if message.reply_to_message is None:
            try:
                user_name = message.from_user.username
                who = message.text.split('@', maxsplit=1)[1]

                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/slap.jpg', 'rb')
                await message.answer_photo(photo, f'😤 Буллер @{user_name} дал подзатыльник @{who}')
                await message.delete()

            except IndexError:
                await message.reply('⚠️ Неверный синтаксис\n\nИспользуйте: */slap @username*', parse_mode='Markdown')

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Пользователь отсутствует в базе данных!\n\nРешение: *введите команду /reg*', parse_mode='Markdown')
            
        else:
            try:
                user_name = message.from_user.username
                change_name = message.reply_to_message.from_user.username
                
                await asyncio.sleep(2)
                photo = open(f'{dir}imgs/slap.jpg', 'rb')
                await message.answer_photo(photo, f'😤 Буллер @{user_name} дал подзатыльник @{change_name}')
                await message.delete()

            except:
                await message.reply('⚠️ *Произошла неизвестная ошибка! Попробуйте позже*', parse_mode='Markdown')


@dp.message_handler(commands=["setvip"])
async def set_vip(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        user_id = message.from_user.id
        c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
        isadmin = c.fetchone()[0]

        if isadmin >= 5:
            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы выдать или снять VIP статус отправителю!*', parse_mode='Markdown')
            
            else:
                try:
                    change_id = message.reply_to_message.from_user.id

                    admin_name = message.from_user.username
                    give_name = message.reply_to_message.from_user.username
                    give_vip = message.text.split(maxsplit=1)[1]

                    if int(give_vip) == 1:
                        c.execute(f"UPDATE chat_{chat_id} SET vip = ? WHERE id= ?", (int(give_vip), int(change_id)))
                        db.commit()
                        
                        await message.answer(f'💎 Администратор @{admin_name} выдал <b>VIP статус</b> пользователю @{give_name}', parse_mode= "HTML")
                        await message.delete()
                    
                    elif int(give_vip) == 0:
                        c.execute(f"UPDATE chat_{chat_id} SET vip = ? WHERE id= ?", (int(give_vip), int(change_id)))
                        db.commit()

                        await message.answer(f'💎 Администратор @{admin_name} снял <b>VIP статус</b> пользователю @{give_name}', parse_mode= "HTML")
                        await message.delete()
                    
                    else: 
                        return await message.reply('⚠️ *Неверный аргумент! 1 - выдать/2 - забрать!*', parse_mode='Markdown')

                except IndexError:
                    return await message.reply('⚠️ Неверный синтаксис!\n\n*/setvip <1 - выдать/2 - забрать>*', parse_mode='Markdown')

        else:
            return await message.reply('⚠️ *У вас нет 5-ого и выше уровня доступа!*', parse_mode='Markdown')


@dp.message_handler(commands=["checkvip"])
async def check_vip(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 1:
            if message.reply_to_message is None:
                await message.reply('⚠️ *Ответьте на сообщение, чтобы узнать состояние VIP статуса отправителя!*', parse_mode='Markdown')

            else:
                check_id = message.reply_to_message.from_user.id
                check_name = message.reply_to_message.from_user.username

                c.execute(f"SELECT vip FROM chat_{chat_id} WHERE id = {check_id}")
                nick_check = c.fetchone()[0]

                if int(nick_check) == 1:
                    await message.answer(f'😍 У пользователя @{check_name} имеется VIP статус')
                    await message.delete()
                
                elif int(nick_check) == 0:
                    await message.answer(f'😔 У пользователя @{check_name} отсутствует VIP статус')
                    return await message.delete()

        else:
            return await message.reply('⚠️ *У вас нет 1-ого и выше уровня доступа!*', parse_mode='Markdown')


@dp.message_handler(commands=["unban"])
async def unban_mem(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 3:
            try:
                chat_id = message.chat.id
                banmember_id = message.text.split(maxsplit=1)[1]
                user_name = message.from_user.username

                bot.unban_chat_member(chat_id, banmember_id)

                await message.answer(f'🥰 Администратор @{user_name} разбанил пользователя с ID <b>{banmember_id}', parse_mode= "HTML")
                await message.delete()
            
            except IndexError:
                await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */unban <user id>*", parse_mode='Markdown')

        else:
            await message.reply("⚠️ *У вас нет 3-его и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=['chance'])
async def chance(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            user_name = message.from_user.username
            resul_rand = random.randint(0, 100)
            reson = message.text.split(maxsplit=1)[1]

            if int(resul_rand) >=90:
                await message.answer(f'🙀 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=80 and int(resul_rand) <=89:
                await message.answer(f'😀 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=70 and int(resul_rand) <=79:
                await message.answer(f'😄 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=60 and int(resul_rand) <=69:
                await message.answer(f'😅 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=50 and int(resul_rand) <=59:
                await message.answer(f'😌 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=40 and int(resul_rand) <=49:
                await message.answer(f'😒 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=30 and int(resul_rand) <=39:
                await message.answer(f'😔 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=20 and int(resul_rand) <=29:
                await message.answer(f'😫 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            elif int(resul_rand) >=10 and int(resul_rand) <=19:
                await message.answer(f'😢 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()
            
            elif int(resul_rand) <=9:
                await message.answer(f'😭 @{user_name}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
                await message.delete()

            else:
                return 0

        except IndexError:
            await message.reply("⚠️ Неверный синтаксис!\n\n/chance *<текст>*", parse_mode='Markdown')


@dp.message_handler(commands=['welcome'])
async def get_welcome(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 2:
            chat_id = message.chat.id
            chat_id=str(chat_id)

            res_chat_id = ''
            for i in range(0, len(chat_id)): 
                if i != 0: 
                    res_chat_id = res_chat_id + chat_id[i]

            c.execute(f"SELECT welcome FROM config WHERE id = {res_chat_id}")
            welcome = c.fetchone()[0]

            await message.answer(f'👋 <b>Текущее приветствие - <u>{welcome}</u></b>', parse_mode= "HTML")
            await message.delete()

        else:
            await message.reply("⚠️ *У вас нет 2-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=['setwelcome'])
async def setwelcome(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin[0] >= 4:
            try:
                chat_id = message.chat.id
                chat_id=str(chat_id)

                res_chat_id = ''
                for i in range(0, len(chat_id)): 
                    if i != 0: 
                        res_chat_id = res_chat_id + chat_id[i]
                
                user_name = message.from_user.username
                c.execute(f"SELECT welcome FROM config WHERE id = {res_chat_id}")
                old_welcome = c.fetchone()[0]

                new_welcome = message.text.split(maxsplit=1)[1]

                welcome_info = (str(new_welcome), int(res_chat_id))
                c.execute("UPDATE config SET welcome = ? WHERE id = ?", (welcome_info))
                db.commit()
                

                await message.answer(f'😒 <b>Старое приветствие - <u>{old_welcome}</u></b>\n😃 <b>Новое приветствие - <u>{new_welcome}</u></b>\n\n😇 <b>Изменил -</b> @{user_name}', parse_mode= "HTML")
                await message.delete()

            except IndexError:
                return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */setwelcome <новое приветствие>*", parse_mode='Markdown')

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        else:
            await message.reply("⚠️ *У вас нет 4-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=['setrules'])
async def setrules(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        izn_chat_id = message.chat.id
        izn_chat_id=str(izn_chat_id)

        chat_id = ''
        for i in range(0, len(izn_chat_id)): 
            if i != 0: 
                chat_id = chat_id + izn_chat_id[i]

        try:
            user_id = message.from_user.id
            c.execute(f"SELECT id FROM chat_{chat_id} WHERE id = {user_id}")
            isadmin = c.fetchone()[0]

        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        if isadmin >= 5:
            try:
                chat_id = message.chat.id
                chat_id=str(chat_id)

                res_chat_id = ''
                for i in range(0, len(chat_id)): 
                    if i != 0: 
                        res_chat_id = res_chat_id + chat_id[i]
                
                user_name = message.from_user.username
                c.execute(f"SELECT rules FROM config WHERE id = {res_chat_id}")
                old_rules = c.fetchone()[0]

                new_rules = message.text.split(maxsplit=1)[1]

                rules_info = (str(new_rules), int(res_chat_id))
                
                c.execute("UPDATE config SET rules = ? WHERE id = ?", (rules_info))
                db.commit()
                

                await message.answer(f'😒 <b>Старые правила - <u>{old_rules}</u></b>\n😃 <b>Новые правила - <u>{new_rules}</u></b>\n\n😇 <b>Изменил -</b> @{user_name}', parse_mode= "HTML")
                await message.delete()

            except IndexError:
                return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: */setrules <новые правила>*", parse_mode='Markdown')

            except sqlite3.OperationalError:
                return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

        else:
            return await message.reply("⚠️ *У вас нет 5-ого и выше уровня доступа!*", parse_mode='Markdown')


@dp.message_handler(commands=['rankinfo'])
async def rankinfo(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        return await message.reply('<b>❗️ В боте WonderfulBot есть система уровней!\n\n📌 Изначально у вас 0 уровень и 0 EXP. Чтобы достичь 1 уровня необходимо набрать 20 EXP\nИзначально, за 1 сообщение дается 1 EXP, но создатель может изменить количество до 3 EXP за 1 сообщение.\n\nПосле достижения нового уровня, для получения следующего, вам нужно набрать на 200 EXP больше, чем в прошлый раз.\n\nЧтобы проверить свой уровень и количество EXP - введите команду /rank. Также эта информация содержится в /user(/profile). При ответе на сообщение, с помощью данных команд можно узнать чужой уровень и количество EXP</b>', parse_mode= "HTML")



#Перевод в бинарное число
@dp.message_handler(commands=['binar'])
async def binar(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chisl = message.text.split(maxsplit=1)[1]
            
            if izn_chisl.startswith('0b'):
                res = int(str(izn_chisl), 2)
                await message.reply(f'🤩 Перевод двоичного числа в десятичное:\n\n\n<b>🧐 Запрос (двоичное): {izn_chisl}</b>\n\n<b>📌 Перевод (десятичное): {str(res)}</b>', parse_mode= "HTML")
            
            else:
                await message.reply(f'🤩 Перевод десятичного числа в двоичное:\n\n\n<b>🧐 Запрос (десятичное): {izn_chisl}</b>\n\n<b>📌 Перевод (двоичное): {int(izn_chisl):0{9 if int(izn_chisl) > 0 else 10}b}</b>', parse_mode= "HTML")
        
        except IndexError:
            await message.reply('⚠️ <b>Неверный синтаксис!</b>\n\nИспользуйте: /binar <b> (для перевода в двоичное введите любое десятичное число (Пример: 654). Для перевода в десятиченое перед двоичным числом поставьте префикс 0b) </b>', parse_mode= "HTML")
        
        except ValueError:
            await message.reply('⚠️ <b>Ошибка чисел</b>\n\nИспользуйте: /binar <b>(ЧИСЛО/ЧИСЛО с префиксом 0b)</b>', parse_mode= "HTML")


#Анонимное сообщение
@dp.message_handler(commands=['write'])
async def bot_write_cmd(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            say = message.text.split(maxsplit=1)[1]

        except IndexError:
            return await message.reply('⚠️ Неверный синтаксис!\nИспользуйте: /write *<текст>*', parse_mode='Markdown')

        if len(say) <= 256:
            try:
                await message.delete()
                await message.answer(f'🤨 <i>Анонимное сообщение</i>:\n\n<b>{say}</b>', parse_mode= "HTML")
                
            except:
                return await message.reply('⚠️ *Произошла ошибка. Попробуйте позже*', parse_mode='Markdown')

        else:
            return await message.reply('⚠️ Нельзя использовать *более 256 символов*!', parse_mode='Markdown')


#Голосовое сообщение от бота, GTTS
@dp.message_handler(commands=['say'])
async def bot_say_cmd(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            say = message.text.split(maxsplit=1)[1]

        except IndexError:
            return await message.reply('⚠️ Неверный синтаксис!\nИспользуйте: /say *<текст>*', parse_mode='Markdown')
    
        user_id = message.from_user.id
        if len(say) <= 128:
            try: 
                var = gTTS(text = say, lang = 'ru')
                var.save(f'{user_id}.mp3')
                var = open(f'{user_id}.mp3', 'rb')

                await message.answer_audio(var)
                os.remove(f'{user_id}.mp3')

            except:
                return await message.reply('⚠️ *Произошла ошибка. Попробуйте позже*', parse_mode='Markdown')

        else:
            return await message.reply('⚠️ Нельзя использовать *более 128 символов*!', parse_mode='Markdown')

@dp.message_handler(text = ['Правила', 'правила'])
async def every_message(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0: 
                    chat_id = chat_id + izn_chat_id[i]

            c.execute(f"SELECT rules FROM config WHERE id = {chat_id}")
            rules = c.fetchone()[0]
            await message.reply(f'<b>{rules}</b>', parse_mode= "HTML")
        
        except sqlite3.OperationalError:
            return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode='Markdown')


@dp.message_handler()
async def every_message(message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        try:
            izn_chat_id = message.chat.id
            izn_chat_id=str(izn_chat_id)

            chat_id = ''
            for i in range(0, len(izn_chat_id)): 
                if i != 0: 
                    chat_id = chat_id + izn_chat_id[i]

            user_id = message.from_user.id
            exp = 1
            
            await asyncio.sleep(3)
            c.execute(f"UPDATE chat_{chat_id} SET total_exp = total_exp + ? WHERE id= ?", (int(exp), int(user_id)))
            db.commit()
            c.execute(f"UPDATE chat_{chat_id} SET tolvl_exp = tolvl_exp + ? WHERE id= ?", (int(exp), int(user_id)))
            db.commit()

            await asyncio.sleep(1)
            c.execute(f"SELECT tolvl_exp FROM chat_{chat_id} WHERE id = {user_id}")
            messages_check = c.fetchone()[0]
            c.execute(f"SELECT need_exp FROM chat_{chat_id} WHERE id = {user_id}")
            need_check = c.fetchone()[0]

            if int(messages_check) >= int(need_check):
                level = 1
                c.execute(f"UPDATE chat_{chat_id} SET level = level + ? WHERE id= ?", (int(level), int(user_id)))
                db.commit()
                zero = 0
                c.execute(f"UPDATE chat_{chat_id} SET tolvl_exp = ? WHERE id= ?", (int(zero), int(user_id)))
                db.commit()
                dobavka = 200
                c.execute(f"UPDATE chat_{chat_id} SET need_exp = need_exp + ? WHERE id= ?", (int(dobavka), int(user_id)))
                db.commit()

                c.execute(f"SELECT level FROM chat_{chat_id} WHERE id = {user_id}")
                level_check = c.fetchone()[0]

                await message.reply(f'<b>Вы успешно повысили свой уровень!\nТекущий уровень - {level_check}\n\nПродолжайте общаться в том же духе 💖</b>', parse_mode= "HTML")

        except:
            pass


executor.start_polling(dp, skip_updates=True)