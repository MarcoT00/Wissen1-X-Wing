from Agent import Agent
import concurrent.futures
import time
import os
from multiprocessing import Queue

MAP = 1
MAP = 1


def worker(start_pos_index):
    return Agent(
        map_id=MAP,
        start_pos_index=start_pos_index,
        num_episode=100,  # 100
        stochastic_movement=True,  # True
    )


if __name__ == "__main__":
    start_time = time.time()

    if MAP == 1:
        max_workers = os.cpu_count() - 1
        star_pos_list = list(range(1, 6))
    else:
        max_workers = int(os.cpu_count()/2)+1
        star_pos_list = list(range(23))

    print("Max Workers: ", max_workers)

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        # try:
        concurrent.futures.wait(executor.map(worker, star_pos_list))
        # except Exception as ex:
        # print(ex)

    print("--- %s seconds ---" % (time.time() - start_time))
