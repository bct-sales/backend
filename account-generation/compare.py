#! /usr/bin/env py

import csv
import sys


# ./compare.py main.csv a.csv b.csv ...
# checks that main/csv assigns different passwords than a.csv, b.csv, ...


def read_password_table(filename: str) -> dict[int, str]:
    result: dict[int, str] = {}
    with open(filename) as file:
        reader = csv.reader(file)
        for id, password in reader:
            result[int(id)] = password
    return result


filenames = sys.argv[1:]

if len(filenames) < 2:
    print("I need a list of at least two csv files as command line arguments")

main_filename, *other_filenames = filenames

print("Reading files...")
main_table, *other_tables = [read_password_table(filename) for filename in filenames]

print("Comparing...")
clash_count = 0
for other_filename, other_table in zip(other_filenames, other_tables):
    for id, password in main_table.items():
        if id in other_table and password == other_table[id]:
            clash_count += 1
            print(f"Clash {clash_count} for id {id} with file {other_filename}")
