import aiosqlite
from configs.settings import standart_welcome


async def create_chat_in_db(chat_id: int | str, start_info: tuple):
    """
    Создает таблицу чата в БД

    :param chat_id - ID беседы/группы
    :param user_info - Кортеж из следующей информации: id пользователя, username, уровень админки, ник в боте, количество варнов, уровень VIP, общее кол-во exp, кол-во exp необходимые до нового уровня, кол-во exp собранных для нового лвл, уровень
    """

    config_info = (str(chat_id)[1:-1], standart_welcome, "Правила еще не установлены!")

    async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
        await groups_db.execute(f"CREATE TABLE IF NOT EXISTS chat_{str(chat_id)[1:-1]}(id INT, login TEXT, admin INT, nick TEXT, warns INT, vip INT, total_exp INT, tolvl_exp INT, need_exp INT, level INT)")
        await groups_db.execute('CREATE TABLE IF NOT EXISTS config(id INT, welcome TEXT, rules TEXT)')
        await groups_db.execute(f"INSERT INTO chat_{str(chat_id)[1:-1]} (id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (start_info))
        await groups_db.execute("INSERT INTO config (id, welcome, rules) VALUES (?, ?, ?)", (config_info))
        await groups_db.commit()
    
    return True


async def add_user(chat_id: int | str, user_info: tuple):
    """
    Добавляет кортеж из данных пользователя (user_info) в базу данных

    RETURN:
    :user_info, в случае успеха
    :False, в случае ошибки

    :param chat_id - ID беседы/группы
    :param user_info - Кортеж из следующей информации: id пользователя, username, уровень админки, ник в боте, количество варнов, уровень VIP, общее кол-во exp, кол-во exp необходимые до нового уровня, кол-во exp собранных для нового лвл, уровень
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            await groups_db.execute(f"INSERT INTO chat_{str(chat_id)[1:-1]}(id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_info))
            await groups_db.commit()
    
    except aiosqlite.OperationalError:
        return False
    
    return user_info


async def is_user_exists_chat_db(chat_id: int | str, user_id: int | str) -> bool:
    """
    Проверяет, есть ли пользователь (user_id) в таблице чата (chat_id)

    RETURN:
    :True, если пользователь состоит в базе данных беседы
    :False если данные отсутствуют
    :None, если таблицы чата не существует в БД

    :param chat_id - id беседы, в которой состоит пользователь
    :param user_id - id пользователя для проверки
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            is_exist = await groups_db.execute(f"SELECT id FROM chat_{str(chat_id)[1:-1]} WHERE id = ?", (user_id,))
            is_exist = await is_exist.fetchone()
    
    except aiosqlite.OperationalError:
        return None
    
    if is_exist is not None and len(is_exist) > 0: return True
    return False


async def get_config_data(chat_id: int | str):
    """
    Получает данные чата (chat_id) из таблицы config

    RETURN:
    :turple(rules, welcome), если чат есть в базе данных
    :False, если данные отсутствует

    :param chat_id - id беседы
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            data = await groups_db.execute(f"SELECT rules, welcome FROM config WHERE id = '{str(chat_id)[1:-1]}'")
            data = await data.fetchone()
    
    except aiosqlite.OperationalError:
        return False
    
    if data is not None: return data
    return False


async def set_config_data(chat_id: int | str, column: str, data: int | str):
    """
    Изменяет данные чата (chat_id) в таблице config в указанном столбце (column) на data
 
    RETURN:
    :True, если все прошло успешно
    :False, если возникла ошибка

    :param chat_id - id беседы, в которой необходимо изменить данные
    :param column - название колонки, куда нужно вставить значение ('rules' или 'welcome')
    :param data - информация, которую нужно вставить
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            await groups_db.execute(f"UPDATE config SET {column} = ? WHERE id = '{str(chat_id)[1:-1]}'", (data,))
            await groups_db.commit()

    except aiosqlite.OperationalError:
        return False
    
    return True


async def get_member_chat_info(chat_id: int | str, user_id: int | str):
    """
    Возвращает данные пользователя из таблицы чата в БД

    RETURN:
    :turple с данными участника (id, username, admin, nick, warns, vip, total_vip, tolvl_exp, need_exp, level)
    :False, если данные участника не найдены 
    :None, если беседа отстутствует в БД

    :param chat_id - id беседы, в которой состоит пользователь
    :param user_id - id пользователя для проверки
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            data = await groups_db.execute(f"SELECT id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level FROM chat_{str(chat_id)[1:-1]} WHERE id = ?", (user_id,))
            data = await data.fetchone()
    
    except aiosqlite.OperationalError:
        return None
    
    if data is not None: return data
    return False


async def set_member_chat_info(chat_id: int | str, user_id: int | str, column: str, data):
    """
    Изменяет данные пользователя из таблицы чата в БД в указаном столбце (column) на data

    RETURN:
    :True, в случае успешного завершения
    :False, в случае ошибки во время выполнения

    :param chat_id - id беседы, в которой состоит пользователь
    :param user_id - id пользователя для изменения
    :param column - название колонки, куда нужно вставить значение (id, username, admin, nick, warns, vip, total_vip, tolvl_exp, need_exp, level)
    :param data - информация, которую нужно вставить
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            await groups_db.execute(f"UPDATE chat_{str(chat_id)[1:-1]} SET {column} = ? WHERE id = ?", (data, user_id))
            await groups_db.commit()

    except aiosqlite.OperationalError:
        return False
    
    return True


async def get_admin_lvl(chat_id: int | str, user_id: int | str):
    """
    Получает уровень админки пользователя из таблицы чата в БД

    RETURN:
    :int уровня админки пользователя: при успешном завершении
    :False, если данные участника не найдены
    :None, если беседа отстутствует в БД

    :param chat_id - id беседы, в которой состоит пользователь
    :param user_id - id пользователя для проверки
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            lvl = await groups_db.execute(f"SELECT admin FROM chat_{str(chat_id)[1:-1]} WHERE id = ?", (user_id,))
            lvl = await lvl.fetchone()
    
    except aiosqlite.OperationalError: 
        return None
    
    if lvl is None: return False
    return lvl[0]


async def add_message_chat_user(chat_id: int | str, user_id: int | str):
    """
    Добавляет сообщение пользователю в total_exp и tolvl_exp. При условии, что tolvl_exp > need_exp => level увеличивается 

    RETURNS:
    :True: в случае успшного завершения
    :int нового уровня: если получен новый лвл
    :None: если таблицы чата не существует

    :param chat_id - id беседы, в которой состоит пользователь
    :param user_id - id пользователя для добавления
    """

    try:
        async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
            await groups_db.execute(f"UPDATE chat_{str(chat_id)[1:-1]} SET total_exp = total_exp + {1}, tolvl_exp = tolvl_exp + {1} WHERE id = ?", (user_id,))
            await groups_db.commit()
            messages_check = await groups_db.execute(f"SELECT tolvl_exp, need_exp FROM chat_{str(chat_id)[1:-1]} WHERE id = ?", (user_id,))
            messages_check = await messages_check.fetchone()
            
            if messages_check[0] >= messages_check[1]:
                await groups_db.execute(f"UPDATE chat_{str(chat_id)[1:-1]} SET level = level + {1}, tolvl_exp = {0}, need_exp = need_exp + {100} WHERE id = ?", (user_id,))
                await groups_db.commit()
                current_level = await groups_db.execute(f"SELECT level FROM chat_{str(chat_id)[1:-1]} WHERE id = ?", (user_id,))
                current_level = await current_level.fetchone()[0]

                return current_level
    
    except TypeError: return "UserError"
    except aiosqlite.OperationalError: return None

    return True


async def change_warns(chat_id: int | str, user_id: int | str, action: str):
    """
    Добавляет удаляет/предупреждению пользователю, в зависимости от символа в начале аргумента action

    RETURNS:
    :True: в случае успшного завершения
    :False: в случае ошибки
    :None: если таблицы чата не существует

    :param chat_id - id беседы, в которой состоит пользователь
    :param user_id - id пользователя для добавления
    :param action - действие с предупреждением (+/-)
    """

    async with aiosqlite.connect('groups.db', check_same_thread=False) as groups_db:
        await groups_db.execute(f"UPDATE chat_{str(chat_id)[1:-1]} SET warns = warns {action[0]} {1} WHERE id = ?", (user_id,))
        await groups_db.commit()
    
        current_warns = await groups_db.execute(f"SELECT warns FROM chat_{str(chat_id)[1:-1]} WHERE id = ?", (user_id,))
        current_warns = await current_warns.fetchone()
    
    return current_warns[0]
