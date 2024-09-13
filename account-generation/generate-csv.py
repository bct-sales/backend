import random
import sys


MAX_GROUP_SIZE = 99    # Within a group a user must be identifiable with just 2 digits, otherwise the ID format must be redesigned
N_GROUPS = 12
SEED = 48119


def rotate_left(xs, n):
    return [*xs[n:], *xs[:n]]


random.seed(SEED)
group_sizes = [50] * N_GROUPS



if any(group_size > MAX_GROUP_SIZE for group_size in group_sizes):
    print(f"Groups must all be smaller than {MAX_GROUP_SIZE}")
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
