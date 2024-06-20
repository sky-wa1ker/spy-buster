from datetime import datetime as dt
from tinydb import TinyDB, Query
import asyncio

db = TinyDB('db.json')
query = Query()



print(bool(db.search(query.timestamp.exists())[0]['timestamp']))