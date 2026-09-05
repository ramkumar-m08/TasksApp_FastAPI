#SQLite Basics

import sqlite3

#Connecting to DB file,Cursor object-execute SQL commamds
conn=sqlite3.connect("tasks.db")
cur=conn.cursor()
print("Connected to SQLite successfully")


#Creating tasks table and saving(COMMIT) changes
cur.execute("""
  CREATE TABLE IF NOT EXISTS tasks(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      completed BOOLEAN DEFAULT 0)""")
conn.commit()

#CRUD Operations
#Create
cur.execute(
  "INSERT INTO tasks(title,completed) VALUES(?,?)",("Learning SQLite basics",True))
cur.execute(
  "INSERT INTO tasks(title,completed) VALUES(?,?)",("Learning SQL Alchemy basics",False))
conn.commit()

#Read data
cur.execute(
  "SELECT * FROM tasks")
all_tasks=cur.fetchall()
print("All tasks:",all_tasks)

#Update data
cur.execute(
  "UPDATE tasks SET completed=True WHERE id=2")
conn.commit()

print("After Update")
cur.execute(
  "SELECT * FROM tasks")
all_tasks=cur.fetchall()
print("All tasks:",all_tasks)

#Delete Data
cur.execute(
  "DELETE FROM tasks WHERE id=2" )
conn.commit()

print("After Delete")
cur.execute(
  "SELECT * FROM tasks")
all_tasks=cur.fetchall()
print("All tasks:",all_tasks)
#Close the DB connection
conn.close()


