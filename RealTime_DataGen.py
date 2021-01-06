import random
import time
import csv

x_value = 0
total_1 = 1000
total_2 = 1000

fieldnames = ["x_value", "total_1", "total_2"]

with open("data.csv", 'w') as csv_file:
    csv_writter = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writter.writeheader()


while True:
    with open("data.csv", 'a') as csv_file:
        csv_writter = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1,
            "total_2": total_2
        }

        csv_writter.writerow(info)

        x_value += 1
        total_1 += random.randint(-6, 8)
        total_2 += random.randint(-5, 6)
    time.sleep(1)