from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.filters.command import Command, CommandObject

from gtts import gTTS
from random import randint
from os import remove

from filters.chat_type import ChatTypeFilter
from database import set_member_chat_info, get_member_chat_info


router = Router()

# /write
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('write'))
async def bot_write_cmd(message: types.Message, command: CommandObject):
    """
    Написать сообщение с текстом из аргумета text от имени бота\n
    Ограничение в text - 256 символов\n
    
    Аргументы:
    :text - текст для сообщения
    """

    say = command.args
    if say is None or say == False: return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */write <текст>*', parse_mode='Markdown')
    if len(say) >= 256: return await message.reply('⚠️ Нельзя использовать *более 256 символов*!', parse_mode='Markdown')
    try:
        await message.delete()
        return await message.answer(f'🤨 <i>За меня написали</i>:\n\n<b>{say}</b>', parse_mode= "HTML")
    except:
        await message.delete()
        return await message.reply('⚠️ *Произошла ошибка... Попробуйте позже*', parse_mode='Markdown')


# /say
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('say'))
async def bot_say_cmd(message: types.Message, command: CommandObject):
    """
    Создать голосовое сообщение с текстом из аргумета text от имени бота\n
    Ограничение в text - 128 символов\n
    
    Аргументы:
    :text - текст для сообщения
    """
        
    say = command.args

    if say is None or say == False: return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */say <текст>*', parse_mode='Markdown')
    if len(say) >= 128: return await message.reply('⚠️ Нельзя использовать *более 128 символов*!', parse_mode='Markdown')
        
    try:
        voice = gTTS(text = say, lang = 'ru')
        voice.save(f'temp_data\\{message.from_user.id}.mp3')
    except:
        await message.reply('⚠️ *Произошла ошибка. Попробуйте позже*', parse_mode='Markdown')
        try: return remove(f'temp_data\\{message.from_user.id}.mp3')
        except: pass
    
    try:
        await message.answer_audio(audio=FSInputFile(f'temp_data\\{message.from_user.id}.mp3'))
        return remove(f'temp_data\\{message.from_user.id}.mp3')
    except: return await message.reply('⚠️ *Произошла ошибка. Попробуйте позже*', parse_mode='Markdown')


# /binar
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('binar'))
async def binar(message: types.Message, command: CommandObject):
    """
    Преобразовать десятичное число number в двоичное и наоборот\n
    
    Аргументы:
    :number - число для преобразования
    """

    number = command.args
    
    if number is None or number ==  False: return await message.reply('⚠️ <b>Неверный синтаксис!</b>\n\nИспользуйте: <b>/binar (для перевода в двоичное введите любое десятичное число (Пример: 654). Для перевода в десятиченое перед двоичным числом поставьте префикс 0b) </b>', parse_mode= "HTML")
        
    try:
        if number.startswith('0b'): return await message.reply(f'🤩 Перевод двоичного числа в десятичное:\n\n<b>🧐 Запрос (двоичное): {number}</b>\n\n<b>📌 Перевод (десятичное): {int(number, 2)}</b>', parse_mode= "HTML")
        else: return await message.reply(f'🤩 Перевод десятичного числа в двоичное:\n\n<b>🧐 Запрос (десятичное): {number}</b>\n\n<b>📌 Перевод (двоичное): {int(number):0{9 if int(number) > 0 else 10}b}</b>', parse_mode= "HTML")
        
    except ValueError: return await message.reply('⚠️ <b>Ошибка чисел</b>\n\nИспользуйте: /binar <b>(ЧИСЛО/ЧИСЛО с префиксом 0b)</b>', parse_mode= "HTML")
    

# /chance
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('chance'))
async def chance(message: types.Message, command: CommandObject):
    """
    Рандомное число от 0 до 100 с эмодзи в зависимости от процента\n
    
    Аргументы:
    :reason - причина для рандома
    """

    resul_rand = randint(0, 100)
    reson = command.args
    if reson is None or reson == False: return await message.reply("⚠️ Неверный синтаксис!\n\n/chance *<текст>*", parse_mode='Markdown')

    if resul_rand >=90: return await message.answer(f'🙀 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=80: return await message.answer(f'😀 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=70: return await message.answer(f'😄 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=60: return await message.answer(f'😅 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=50: return await message.answer(f'😌 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=40: return await message.answer(f'😒 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=30: return await message.answer(f'😔 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=20: return await message.answer(f'😫 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand >=10: return await message.answer(f'😢 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")
    elif resul_rand <=9:  return await message.answer(f'😭 @{message.from_user.username}, я думаю, что шанс того, что <b>{reson}</b>, равен <b>{resul_rand}%</b>', parse_mode= "HTML")


# /random
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('random', 'rand'))
async def random_number(message: types.Message, command: CommandObject):
    """
    Рандомное число от x до y\n
    
    Аргументы:
    :x - число ОТ которого идет рандом
    :y число ДО которого идет рандом
    """
    
    if command.args is None: return await message.reply("⚠️ Неверный синтаксис!\n\nИспользуйте: **/rand <от> <до>**", parse_mode='Markdown')
        
    from_num, to_num = command.args.split(' ', maxsplit=1)
        
    try: resul_rand = randint(int(from_num), int(to_num))
    except ValueError: return await message.reply("⚠️ Ошибка радиуса или в аргументах используется текст!\n\nИспользуйте: */rand <ОТ> <ДО>*", parse_mode='Markdown')

    return await message.answer(f'🎲 @{message.from_user.username}, ваше рандомное число от <b>{from_num}</b> до <b>{to_num}</b> — <b>{resul_rand}</b>', parse_mode= "HTML")


# /mynick
@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]), Command('mynick'))
async def set_self_nick(message: types.Message, command: CommandObject):
    new_nick = command.args
    if new_nick is None or new_nick == False or new_nick == '': return await message.reply('⚠️ Неверный синтаксис!\n\nИспользуйте: */mynick <новый ник>*!', parse_mode='Markdown')

    old_nick = await get_member_chat_info(message.chat.id, message.from_user.id)
    if old_nick is None: return await message.reply('⚠️ Ваша беседа не зарегистрирована!\n\nРешение: *введите команду /startbot*', parse_mode= "Markdown")

    await set_member_chat_info(message.chat.id, message.from_user.id, 'nick', new_nick)
            
    return await message.answer(f'💡 Пользователь @{message.from_user.username} изменил свой ник с <b>{old_nick[3]}</b> на <b>{new_nick}</b>', parse_mode= "HTML")
