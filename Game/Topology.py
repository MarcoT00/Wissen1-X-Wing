import csv


class Topology:

    start_positions_map_1 = [(32, x) for x in range(4, 10)]
    start_positions_map_2 = [(30, x) for x in range(1, 24)]
    end_positions_map_1 = [(y, 17) for y in range(1, 7)]
    end_positions_map_2 = [(y, 32) for y in range(1, 10)]

    @staticmethod
    def get_map(map_id):
        map_name = "topology" + str(map_id) + ".csv"
        with open(map_name) as csvfile:
            rows = csv.reader(csvfile)
            return [list(row) for row in rows]

    @staticmethod
    def get_start_pos(self, map_id, start_pos_index):
        if map_id == 1:
            pos = self.start_positions_map_1[start_pos_index]
        elif map_id == 2:
            pos = self.start_positions_map_2[start_pos_index]
        return {"x": pos[1], "y": pos[0]}
