# WonderfulBot
WonderfulBot - чат-менеджер для телеграма

В данном менеджере присутствует широкий функционал, с которым вы можете ознакомиться ниже.

Зависимости: **aiogram 3x, pillow, gtts, logging**


# Настройка бота
Главный файл, который используется для запска - src/__main__.py

Настройка находится в файле src/configs/settings.py

**token** - токен бота, можно получить у BotFather

**dir** - директория вашего бота

**admins_id** - список ID пользователей, которые имеют право активировать бота

**version** - версия бота, можете не трогать

**standart_welcome** - стандартное приветствие в беседах при активации бота

**tg_channel** - Telegram канал бота, отображается в /botinfo



**При добавлении в чат, выдайте боту админку, а затем пропишите /startbot**



# Команды пользователей:

# Основное:

/help - список команд

/start - зарегистрироваться в боте

/profile(/user) - посмотреть свой профиль (при ответе на сообщение можно посмотреть профиль отправителя)

/getid(/gid) - узнать ID пользователя

/getnick(/gnick) - узнать ник пользователя

/rank - узнать свой уровень и количество EXP(при ответе на сообщение можно посмотреть уровень и EXP отправителя)

/botinfo - информация о боте

/rankinfo - информация о системе уровней и EXP

Правила - посмотреть правила

# Развлечения:

/mynick <новый ник> - изменить себе ник

/random(/rand) <от> <до> - рандомное число

/chance <text> - узнать вероятность того, что указано в text

/binar <десятичное число или двоичное число (префикс 0b)> - перевести десятичное число в двоичное и наоборот

/say <текст> - отправить голосовое сообщение от лица бота

/write <текст> - отправить текстовое сообщение от лица бота

# РП команды: 
  
/ebaca(/sex) /kiss /slap /kill


# Команды администрации:

  
# 1-ый уровень:

/ahelp - показать список команд

/kick - кикнуть пользователя

/mute <время в минутах> - замутить пользователя

/unmute - снять мут пользователю

/checkvip - проверить наличие VIP статуса

/reg - зарегистрировать пользователя


# 2-ой уровень:

/pin - закрепить сообщение

/unpin - открепить сообщение

/unpinall - открепить все сообщения

/welcome - узнать текущее приветствие
  
/clear <кол-во сообщений> - очистить указанное количество сообщений


# 3-ий уровень:

/ban <время в днях> - забанить пользователя

/unban <id человека, которого нужно разбанить> - разбанить пользователя

/warn - выдать варн пользователю

/unwarn - снять варн пользователю

/setnick <новый ник> - изменить ник пользователю


# 4-ый уровень:
  
/title <новое название> - изменить название группы
  
/description(/desc) <новое описание> - изменить описание группы
  
/setwelcome <новое приветствие> - изменить приветствие


# 5-6 уровень:
  
/setadmin <уровень> - назначить пользователя на админку
  
/setvip <1 - выдать/2 - забрать> - выдать или снять VIP статус
  
/setrules <новые правила> - установить новые правила
