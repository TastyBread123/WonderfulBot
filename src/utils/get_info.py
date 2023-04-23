def get_chat_db_id(chat_id) -> int:
    return_chat_id = ''
    for i in range(0, len(str(chat_id))): 
        if i != 0: 
            return_chat_id = return_chat_id + str(chat_id)[i]
    else:
        return int(return_chat_id)
