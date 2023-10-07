import random
import sys


random.seed(48119)
group_sizes = [50] * 12



if any(group_size >= 100 for group_size in group_sizes):
    print("Groups must all be smaller than 100")
    sys.exit(-1)


with open('passwords.txt') as file:
    passwords = [line.strip() for line in file]

if sum(group_sizes) > len(passwords):
    print("Insufficient passwords in passwords.txt!")
    sys.exit(-1)

random.shuffle(passwords)


table = {}
password_index = 0

for index, group_size in enumerate(group_sizes):
    base_id = 100 * (index + 1)
    for i in range(group_size):
        id = base_id + i
        if id in table:
            print(f"Bug in program: tried to reuse id {id} twice")
            sys.exit(-1)
        password = passwords[password_index]
        password_index += 1
        table[id] = password


for id, password in table.items():
    print(f'{id},{password}')
