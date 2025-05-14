import sqlite3
from datetime import datetime, timedelta

current_date = datetime.now()

connection = sqlite3.connect(r'Database\EMEAS.db')

cursor = connection.cursor()
cursor.execute("SELECT MAX(dt) FROM metadata")
largest_dt = cursor.fetchone()[0]

if current_date - timedelta(days=330) >= datetime.strptime(largest_dt, "%Y-%m-%d"):
    print("The largest datetime value in the metadata table is more than 330 days old.")

# connection.close()

