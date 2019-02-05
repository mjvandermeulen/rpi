#!/usr/local/bin env python3

r = {
    "name": "honey",
    "setpoint": "180",
}

if r["name"] in ["cbd", ""]:
    print("bingo")

# my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# for index, value in enumerate(my_list):
#     print("index: {}  value: {} my_list: {}".format(index, value, my_list))
#     del(my_list[index])
# print(my_list)

# r = range(5)
# print(r)
# r = 3.4
# print(f"{r:3.10f}")


# import csv
# with open('./csv_automation_settings/temperature_profiles.csv') as profile_file:
#     csv_reader = csv.reader(profile_file, delimiter=',')
#     line_count = 0
#     profiles = []
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#         else:
#             profiles.append({})
#             for cell in row:
#                 print("cell: {}".format(cell))
#                 profiles[-1][cell] = cell
#         line_count += 1
#     print(f'Processed {line_count} lines.')
#     print(profiles)

# import csv
# with open('./csv_automation_settings/temperature_profiles.csv') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for i in range(5):
#         print('*****')
#     for row in csv_reader:
#         print('=========')
#         if True:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         for key in row:
#             print("key: {} --- row[key]: {}".format(key, row[key]))
#         line_count += 1
#     print(f'Processed {line_count} lines.')

def gen():
    print("generator 0")
    yield 1
    print("generator 1")
    yield 2
    print("generator 2")
    yield 3
    print("generator 3")
    yield 4
    print("generator 4 (Only reached at end of iteration over generator")
    # OR:
    #     for i in range(4):
    #         yield i + 1


# if you replace g with gen() in the next part,
# it will produce 1; 1; 1 2 3 4
# since you start with a new generator every time.


# g = gen()

# print(next(g), ' <- next(g)')
# print(next(g), ' <- next(g)')

# for i in g:
#     print(i, end=' <- i in g ')
# print('done')
# # 1
# # 2
# # 3 4

# print("=====")

# g = gen()
# for i in range(5):
#     try:
#         print(next(g), ' <- next(g) ')
#     except StopIteration:
    print("end of generator reached")
