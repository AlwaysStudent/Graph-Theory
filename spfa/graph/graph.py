import csv


class Graph:
    def __init__(self, edge=None):
        if edge is None:
            edge = []
        self.edge = edge
        self.vertex = []
        self.vertex_number = 0
        
    def read_from_csv(self, file_path: str):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            vertex_number = 0
            for row in reader:
                try:
                    vertex_number = int(row[1])
                except ValueError:
                    continue
                if vertex_number < int(row[1]):
                    vertex_number = int(row[1])
            self.edge = [dict() for i in range(vertex_number + 1)]
            
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    begin, end, weight = int(row[1]), int(row[2]), int(row[3])
                except ValueError:
                    continue
                self.edge[begin][end] = weight
        
        self.vertex_number = vertex_number
            

def main():
    g = Graph()
    g.read_from_csv("../spfa/data/graph-generated.csv")


if __name__ == '__main__':
    main()
        