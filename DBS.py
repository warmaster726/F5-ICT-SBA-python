import sqlite3
from datetime import datetime, timedelta

def checking():
    current_date = datetime.now()
    connection = sqlite3.connect(r'Database\EMEAS.db')
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(dt) FROM metadata")
    largest_dt = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    if current_date - timedelta(days=330) >= datetime.strptime(largest_dt, "%Y-%m-%d"):
        return True
    else:
        return False
    


