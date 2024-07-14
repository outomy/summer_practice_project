async def dialog_history_get():
    try:
        with open(f'app/documents/bd.txt', 'r', encoding='utf-8') as db_file:
            lines = db_file.readlines()
            content = ' '.join([line.rstrip() + '. ' for line in lines])
            return content
    except FileNotFoundError:
        return None


async def dialog_history_write(query: str):
    try:
        with open(f'app/documents/bd.txt', 'a', encoding='utf-8') as db_file:
            db_file.write(query + '\n')

    except FileNotFoundError:
        with open(f'app/documents/bd.txt', 's', encoding='utf-8') as db_file:
            pass


async def dialog_history_clear():
    try:
        with open(f'app/documents/bd.txt', 'w', encoding='utf-8') as db_file:
            db_file.truncate(0)
    except FileNotFoundError:
        pass