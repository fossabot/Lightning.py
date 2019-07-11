import dataset
import os

DB_URL = dataset.connect("sqlite:///config/guild_config.sqlite3")

def write_to_guild_config(guid: int, column: str, input: str):
    DB_URL['config'].insert(dict(guild_id=guid, column=input))

def remove_from_guild_config(guid: int, column: str):
    DB_URL['config'].delete(guild_id=guid, column=input)

def read_one_guild_config(guid, column: str):
    DB_URL['config'].find(guild_id=guid)