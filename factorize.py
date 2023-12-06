import logging
import concurrent.futures
from multiprocessing import cpu_count, current_process
from time import time

NUMS = [12810650, 2558802, 1999904, 10651060]

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def factorize(*number):
    logger.debug(f"Current process={current_process().pid}")
    list_num_list = []
    for i in number:
        num_list = [x for x in range(1, i+1) if i % x == 0]
        logger.debug(f"Number: {i} divides on {num_list} entirely")
        list_num_list.append(num_list)
    return list_num_list


if __name__ == '__main__':
    print("Sync:")
    timer = time()
    a, b, c, d = factorize(*NUMS)
    print(f'\nDone for the time {time() - timer} s')

    # assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    # assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    # assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    # assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
    #              380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    print("\n\nAsync: ")
    timer = time()
    with concurrent.futures.ProcessPoolExecutor(cpu_count()) as executor:
        executor.map(factorize, NUMS)
    print(f'\nDone for the time {time() - timer} s\n')
