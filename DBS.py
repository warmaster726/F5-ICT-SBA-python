import sqlite3
from datetime import datetime, timedelta

def checking():
    current_date = datetime.now()
    connection = sqlite3.connect('EMEAS.db')
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(dt) FROM metadata")
    largest_dt = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    if current_date - timedelta(days=330) >= datetime.strptime(largest_dt, "%Y-%m-%d %H:%M:%S"):
        return True
    else:
        return False
    
def sqlrun(query, params=()):
    connection = sqlite3.connect('EMEAS.db')
    cursor = connection.cursor()
    cursor.execute(query, params)

    if query.strip().lower().startswith('select'):
        return cursor.fetchall()

    connection.commit()
    cursor.close()
    connection.close()

