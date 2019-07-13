import dataset

DB_URL = dataset.connect("sqlite:///config/guild_config.sqlite3")

def write_to_guild_config(guid: int, column: str, input: str):
    res = DB_URL['config'].find_one(guild_id=guid)
    if res is None:
        DB_URL['config'].insert(dict(guild_id=guid, column=input))
    else:
        DB_URL['config'].update(dict(guild_id=guid, column=input), ['guild_id'])

def remove_from_guild_config(guid: int, column: str):
    try:
        res = DB_URL['config'].find(guild_id=guid)
        for config in res:
            DB_URL['config'].delete(column=config[f'{column}'])
    except:
        return False

def read_guild_config(guid: int, column: str):
    res = DB_URL['config'].find_one(guild_id=guid)
    if res is None:
        return False
    try:
        return res[f'{column}']
    except KeyError:
        return False
