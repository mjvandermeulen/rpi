#!/usr/local/bin env python3

# by mjvandermeulen
# there is a package that has a wrapper like this:
# https://stackoverflow.com/a/27698681


class Peekable_generator_wrapper(object):

    def __init__(self, generator):
        self._generator = generator()
        self.peek = None

        try:
            self.peek = next(self._generator)
        except StopIteration:
            self.peek = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self.peek:
            raise StopIteration
        return_value = self.peek
        try:
            self.peek = next(self._generator)
        except StopIteration:
            self.peek = None
        return return_value


def pi_generator(3, 4, 5):
    yield(3)
    yield(1)
    yield(4)
    yield(1)
    yield(5)
    # ...

# MAIN


gen_with_peek_parameter = Peekable_generator_wrapper(pi_generator)

for g in gen_with_peek_parameter:
    print("loop g: {}".format(g))
    print("     peekable_g.peek: {}".format(gen_with_peek_parameter.peek))
print("end loop")

# # d.items

# d = {0: 'aap', 1: 'noot', 2: 'mies'}
# for indx, value in d.items():
#     print("{} {}".format(indx, value))


# import pickle


# def read_temperature_control_data_from_file_pickle_generator(filename):
#     try:
#         with open(filename, 'rb') as f:
#             loads = 0
#             while True:
#                 # loads += 1
#                 try:
#                     row = pickle.load(f)
#                     version = row.get("d_x", False)
#                     print(loads)
#                     print(version)
#                     if version:
#                         print("Bingo")
#                     yield row
#                 except EOFError:
#                     break
#     except IOError:
#         print("file {} not found in read_temperature_control_data_from_file_pickle_generator".format(filename))


# gen = read_temperature_control_data_from_file_pickle_generator(
#     './measurements/temperature_controller/test-feb-2019-02-07_10-55.pickle')


# for row in gen:
#     for key in row:
#         print(key + '; ', end='')

# The get() method on dicts
# and its "default" argument

# name_for_userid = {
#     382: "Alice",
#     590: "Bob",
#     951: "Dilbert",
# }


# def greeting(userid):
#     return "Hi %s!" % name_for_userid.get(userid, "there")


# print(greeting(382))
# # "Hi Alice!"

# print(greeting(333333))
# # "Hi there!"

# import argparse

# parser = argparse.ArgumentParser(
#     description='Plot temperature data written by the temperature controller class')
# parser.add_argument('filename', type=open,
#                     help='required filename (including the path)')
# parser.add_argument('--temp-only', '-t',  # turned into temp_only with an underscore
#                     help='display temperature plot only. (default: show pid plot as well)',
#                     action="store_true")
# parser.add_argument('--kpid', '-k',
#                     help='display the k_p, k_i and k_d values',
#                     action="store_true")
# parser.add_argument('--interval', '-i',
#                     help='display the interval and min_switch_time values',
#                     action="store_true")
# args = parser.parse_args()
# print(args)
# print(args.filename)

# parser.add_argument('--foo', nargs=2, help=)
# parser.add_argument('--bar', nargs=3)
# print(parser.parse_args('--bar c d e --foo a b'.split()))


# import csv
# r = {
#     "name": "honey",
#     "setpoint": "180",
# }

# if r["name"] in ["cbd", ""]:
#     print("bingo")

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
# with open('./csv_automation/temperature_profiles.csv', encoding='utf-8-sig') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     line_count = 0
#     for i in range(5):
#         print('*****')
#     for row in csv_reader:
#         print(row)
#         print(row["skip"])
#         print(row["name"])
#         print('=========')
#         if True:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         for key in row:
#             print("key: {} --- row[key]: {}".format(key, row[key]))
#         line_count += 1
#     print(f'Processed {line_count} lines.')

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


# def gen():
#     print("generator 0")
#     yield 1
#     print("generator 1")
#     yield 2
#     print("generator 2")
#     yield 3
#     print("generator 3")
#     yield 4
#     print("generator 4 (Only reached at end of iteration over generator")
#     # OR:
#     #     for i in range(4):
#     #         yield i + 1


# # if you replace g with gen() in the next part,
# # it will produce 1
# # 1
# # 1 2 3 4
# # since you start with a new generator every time.


# g = gen()

# print(next(g), ' <- next(g)')
# print(next(g), ' <- next(g)')
# print(next(g), ' <- next(g)')
# print(next(g), ' <- next(g)')
# try:
#     print(next(g), ' <- next(g)')
# except StopIteration:
#     print("STOP!")
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
#         print("end of generator reached")
