import sqlite3

from configs.settings import standart_welcome
from utils import get_info

def create_chat_in_db(chat_id: int | str, start_info: tuple):
    groups_db = sqlite3.connect('groups.db', check_same_thread=False)
    config_info = (get_info.get_chat_db_id(chat_id), standart_welcome, "Правила еще не установлены!")
    groups_db.execute(f"CREATE TABLE IF NOT EXISTS chat_{get_info.get_chat_db_id(chat_id)}(id INT, login TEXT, admin INT, nick TEXT, warns INT, vip INT, total_exp INT, tolvl_exp INT, need_exp INT, level INT)")                
    groups_db.execute(f"INSERT INTO chat_{get_info.get_chat_db_id(chat_id)} (id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (start_info))
    groups_db.execute("INSERT INTO config (id, welcome, rules) VALUES (?, ?, ?)", (config_info))
    groups_db.commit()
    return True

def add_user(chat_id: int | str, user_info: tuple):
    """
    Добавляет кортеж из данных пользователя (user_info) в базу данных

    RETURN:
    :user_info, в случае успеха
    :False, в случае ошибки

    :param chat_id - ID беседы/группы
    :param user_info - Кортеж из следующей информации: id пользователя, username, уровень админки, ник в боте, количество варнов, уровень VIP, общее кол-во exp, кол-во exp необходимые до нового уровня, кол-во exp собранных для нового лвл, уровень
    """
    try:
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        groups_db.execute(f"INSERT INTO chat_{get_info.get_chat_db_id(chat_id)}(id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_info))
        groups_db.commit()
        groups_db.close()
        return user_info
    except sqlite3.OperationalError: return False


def is_user_exists_chat_db(chat_id: int | str, user_id: int | str) -> bool:
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
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        is_exist = groups_db.execute(f"SELECT id FROM chat_{get_info.get_chat_db_id(chat_id)} WHERE id = ?", (user_id,)).fetchone()
        groups_db.close()
        if is_exist is not None and len(is_exist) > 0: return True

        return False
    except sqlite3.OperationalError: return None


def get_config_data(chat_id: int | str):
    """
    Получает данные чата (chat_id) из таблицы config

    RETURN:
    :turple(rules, welcome), если чат есть в базе данных
    :False, если данные отсутствует

    :param chat_id - id беседы
    """
    try:
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        data = groups_db.execute(f"SELECT rules, welcome FROM config WHERE id = '{get_info.get_chat_db_id(chat_id)}'").fetchone()
        groups_db.close()
        if data is not None: return data

        return False
    except sqlite3.OperationalError: return False


def set_config_data(chat_id: int | str, column: str, data):
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
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        groups_db.execute(f"UPDATE config SET {column} = ? WHERE id = '{get_info.get_chat_db_id(chat_id)}'", (data,))
        groups_db.commit()
        groups_db.close()
        return True

    except sqlite3.OperationalError: return False

def get_member_chat_info(chat_id: int | str, user_id: int | str):
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
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        data = groups_db.execute(f"SELECT id, login, admin, nick, warns, vip, total_exp, tolvl_exp, need_exp, level FROM chat_{get_info.get_chat_db_id(chat_id)} WHERE id = ?", (user_id,)).fetchone()
        groups_db.close()
        if data is not None: return data

        return False
    except sqlite3.OperationalError: return None


def set_member_chat_info(chat_id: int | str, user_id: int | str, column: str, data):
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
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        groups_db.execute(f"UPDATE chat_{get_info.get_chat_db_id(chat_id)} SET {column} = ? WHERE id = ?", (data, user_id))
        groups_db.commit()
        groups_db.close()
        return True

    except sqlite3.OperationalError: return False


def get_admin_lvl(chat_id: int | str, user_id: int | str):
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
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        lvl = groups_db.execute(f"SELECT admin FROM chat_{get_info.get_chat_db_id(chat_id)} WHERE id = ?", (user_id,)).fetchone()
        groups_db.close()
        if lvl is None: return False

        return lvl[0]
    except sqlite3.OperationalError: return None


def add_message_chat_user(chat_id: int | str, user_id: int | str):
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
        groups_db = sqlite3.connect('groups.db', check_same_thread=False)
        groups_db.execute(f"UPDATE chat_{get_info.get_chat_db_id(chat_id)} SET total_exp = total_exp + {1}, tolvl_exp = tolvl_exp + {1} WHERE id = ?", (user_id,)).fetchone()
        groups_db.commit()
        messages_check = groups_db.execute(f"SELECT tolvl_exp, need_exp FROM chat_{get_info.get_chat_db_id(chat_id)} WHERE id = ?", (user_id,)).fetchone()
        
        if messages_check[0] >= messages_check[1]:
            groups_db.execute(f"UPDATE chat_{get_info.get_chat_db_id(chat_id)} SET level = level + {1}, tolvl_exp = {0}, need_exp = need_exp + {100} WHERE id = ?", (user_id,))
            groups_db.commit()
            current_level = groups_db.execute(f"SELECT level FROM chat_{get_info.get_chat_db_id(chat_id)} WHERE id = ?", (user_id,)).fetchone()[0]
            groups_db.close()
            return current_level
        
        groups_db.close()
        return True
    except sqlite3.OperationalError: return None
    except TypeError: return "UserError"


def change_warns(chat_id: int | str, user_id: int | str, action: str):
    """
    Добавляет удаляет/предупреждению пользователю, в зависимости от +/- в начале аргумента action

    RETURNS:
    :True: в случае успшного завершения
    :False: в случае ошибки
    :None: если таблицы чата не существует
    """

    groups_db = sqlite3.connect('groups.db', check_same_thread=False)

    if action.startswith('-'):
        groups_db.execute(f"UPDATE chat_{get_info.get_chat_db_id(chat_id)} SET warns = warns - {1} WHERE id = ?", (user_id,))
        groups_db.commit()
    elif action.startswith('+'):
        groups_db.execute(f"UPDATE chat_{get_info.get_chat_db_id(chat_id)} SET warns = warns + {1} WHERE id = ?", (user_id,))
        groups_db.commit()
    
    current_level = groups_db.execute(f"SELECT warns FROM chat_{get_info.get_chat_db_id(chat_id)} WHERE id = ?", (user_id,)).fetchone()[0]
    groups_db.close()
    return current_level
