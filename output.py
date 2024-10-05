import csv
import os

output_file = os.path.join('keyresult.csv')


def write_result(data):
    """Write new scrapped data to final result file"""

    headers = ["Author Username", "Follower Count", "Following Count", "Like Count"]
    with open(output_file, 'a', newline='') as file:
        file_is_empty = os.stat(output_file).st_size == 0
        csv_writer = csv.writer(file, delimiter=',')
        if file_is_empty:
            csv_writer.writerow(headers)
        csv_writer.writerow(data)

