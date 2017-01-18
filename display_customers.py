#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('db.sqlite3')
print("Opened database successfully")

cursor = conn.execute("SELECT name, demand, position  from problems_customer")
for row in cursor:
   print("NAME = ", row[0])
   print("DEMAND = ", row[1])
   print("POSITION = ", row[2], "\n")

print("Operation done successfully");
conn.close()
