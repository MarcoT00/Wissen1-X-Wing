from AgentV2 import Agent
import concurrent.futures
import time
import os


def get_max_workers(MAP):
    if MAP == 1:
        max_workers = os.cpu_count() - 1
        star_pos_list = list(range(0, 6))
    else:
        max_workers = int(os.cpu_count() / 3)
        star_pos_list = list(range(23))
    return max_workers, star_pos_list


class Learn:
    def __init__(self):
        self.MAP = None

    def worker(self, start_pos_index):
        return Agent(
            map_id=self.MAP,
            start_pos_index=start_pos_index,
            num_episode=100,  # 100
            stochastic_movement=True,  # True
        )

    def multi_processing(self, map):
        start_time = time.time()
        self.MAP = map
        max_workers, star_pos_list = get_max_workers(self.MAP)
        print("Max Workers: ", max_workers)
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            try:
                concurrent.futures.wait(executor.map(self.worker, star_pos_list))
            except Exception as ex:
                print(ex)
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    learn = Learn()
    #learn.multi_processing(map=1)
    learn = Learn()
    learn.multi_processing(map=2)