import sqlite3
import json

connection = sqlite3.connect('seleniumdb.db')
cursor = connection.cursor()


def export_json_data():
    cursor.execute("SELECT * from information")
    fetched_data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data_list = []
    for row in fetched_data:
        data_list.append(dict(zip(column_names, row)))

    # Export data to a JSON file
    with open('data.json', 'w') as json_file:
        json.dump(data_list, json_file, indent=4)

    # Close the connection
    connection.close()



export_json_data()
