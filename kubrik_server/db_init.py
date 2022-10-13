import sqlite3

connection = sqlite3.connect('kubrik.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

lines = open("drives.txt", "r").read().split("\n")
for line in lines:
    query = query = "INSERT INTO google_drive_ids VALUES ('"+line+"', 1)"
    connection.execute(query)

cur = connection.cursor()
connection.commit()
connection.close()