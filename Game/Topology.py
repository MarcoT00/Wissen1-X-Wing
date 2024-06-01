import csv
class Topology:
    start_map_1 = []

    def getStartingPos(self, map, index):
        pass
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
