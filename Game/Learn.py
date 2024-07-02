from Agent import Agent
import concurrent.futures
import time
import os
from multiprocessing import Queue

MAP = 2


def worker(start_pos_index):
    return Agent(start_pos_index, MAP)


if __name__ == "__main__":
    start_time = time.time()
    max_workers = os.cpu_count() - 1
    star_pos_list = [i for i in range(23)]

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        try:
            concurrent.futures.wait(executor.map(worker, star_pos_list))
        except Exception as ex:
            print(ex)

    print("--- %s seconds ---" % (time.time() - start_time))
