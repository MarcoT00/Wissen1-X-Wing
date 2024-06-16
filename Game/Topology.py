import csv


class Topology:

    start_positions_map_1 = [(32, x) for x in range(4, 10)]
    start_positions_map_2 = [(30, x) for x in range(1, 24)]
    end_positions_map_1 = [(x, 17) for x in range(1, 7)]
    end_positions_map_2 = [(x, 32) for x in range(1, 10)]

    @staticmethod
    def get_starting_pos(self, map_id, starting_pos_index):
        if map_id == 1:
            return self.start_positions_map_1[starting_pos_index]
        elif map_id == 2:
            return self.start_positions_map_2[starting_pos_index]

    @staticmethod
    def get_map(map_id):
        map_name = "topology" + str(map_id) + ".csv"
        with open(map_name) as csvfile:
            rows = csv.reader(csvfile)
            res = [list(row) for row in rows]
        return res

    @staticmethod
    def get_end_positions(self, map_id):
        if map_id == 1:
            return self.end_positions_map_1
        elif map_id == 2:
            return self.end_positions_map_2
