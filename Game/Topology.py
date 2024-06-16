import csv
class Topology:
    start_map_1 = [[32, x] for x in range(4,10)]
    start_map_2 = [[30, x] for x in range(1,24)]

    end_map_1 = [[x, 17] for x in range(1,7)]
    end_map_2 = [[x, 32] for x in range(1, 10)]

    def get_starting_pos(self, selected_map, index):
        if selected_map == 1:
            return self.start_map_1[index]
        elif selected_map == 2:
            return self.start_map_2[index]

    @staticmethod
    def get_map(id):
        map_name = None
        if id == 1:
            map_name = "topology1.csv"
        elif id == 2:
            map_name = "topology2.csv"
        with open(map_name) as csvfile:
            rows = csv.reader(csvfile)
            res = [list(row) for row in rows]
            print(res)
        return res
