import sqlite3
import constants

conn = sqlite3.connect(constants.DATABASE_NAME)

cursor = conn.cursor()
cursor.execute("SELECT * FROM IP_INFO")

rows = cursor.fetchall()

for row in rows:
    print(row)