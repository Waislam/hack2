import sqlite3

connection = sqlite3.connect('seleniumdb.db')
cursor = connection.cursor()


def retrieve_data():
    cursor.execute("SELECT * from information")
    fetched_data = cursor.fetchall()
    for row in fetched_data:
        print('every row', row)


retrieve_data()