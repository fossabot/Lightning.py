import dataset

DB_URL = dataset.connect("sqlite:///config/guild_config.sqlite3")

def write_to_guild_config(guid: int, column: str, input: str):
    DB_URL['config'].insert(dict(guild_id=guid, column=input))

def remove_from_guild_config(guid: int, column: str):
    try:
        res = DB_URL['config'].find(guild_id=guid)
        for config in res:
            DB_URL['config'].delete(column=config[f'{column}'])
    except:
        return False

def read_guild_config(guid: int):
    try:
        result = DB_URL['config'].find(guild_id=guid)
        return result
    except:
        return False

def exist_in_guild_config(guid: int, column: str):
    try:
        res = DB['config'].find(guild_id=guid)
        for conf in res:
            return conf[f'{column}']
    except:
        return False