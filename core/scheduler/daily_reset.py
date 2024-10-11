import sqlite3

conn = sqlite3.connect('data.sqlite', check_same_thread=False)
cur = conn.cursor()

