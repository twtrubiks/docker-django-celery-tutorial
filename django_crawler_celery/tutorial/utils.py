import csv
import os


def create_csv(filename, rows):
    dir_name = os.path.dirname(filename)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(filename, 'w') as csv_file:
        spam_writer = csv.writer(csv_file)
        spam_writer.writerow(['name', 'full_name', 'url', 'description'])
        for row in rows:
            spam_writer.writerow(row)
    return filename
