import hashlib
import asyncio
import sqlite3


async def hash_password(username, password):
      salted_password = f"{username}${password}".encode('utf-8')
      hashed_password = hashlib.sha256(salted_password).hexdigest()
      return hashed_password
