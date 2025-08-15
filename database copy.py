import sqlite3
from datetime import datetime 

connection = sqlite3.connect('typing_info.db')

cursor = connection.cursor()

table1 = '''CREATE TABLE IF NOT EXISTS
                typing_stats(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                wpm INTEGER,
                accuracy INTEGER,
                time_stamp TEXT
                )

'''

cursor.execute(table1)
connection.commit()
connection.close()


def store_data(wpm_real, accuracy_real):
    connection = sqlite3.connect('typing_info.db')
    cursor = connection.cursor()  

    current_time = datetime.now().isoformat(timespec="seconds")
    cursor.execute(
        "INSERT INTO typing_stats (wpm, accuracy, time_stamp) VALUES (?, ?, ?)",
        (int(wpm_real), int(round(accuracy_real)), current_time)
    )

    connection.commit()
    connection.close()


def get_last10():
    connection = sqlite3.connect('typing_info.db')
    cursor = connection.cursor()
    cursor.execute(
        "SELECT time_stamp, wpm, accuracy FROM typing_stats ORDER BY time_stamp DESC LIMIT 10"
    )
    rows = cursor.fetchall()
    connection.close()
    return rows

