from queue import PriorityQueue

class TemporalNetwork:
    """
    represents a simple temporal network as a graph.
    """

    def __init__(self) -> None:
        self.nodes : list[int] = []
        self.labels : dict[int, str] = {}
        self.edges = {}

    # ======= #
    # cloning #
    # ======= #

    def copy(self):
        """
        return a copy of the network.
        """
        new_network = TemporalNetwork()
        new_network.nodes = self.nodes.copy()
        new_network.labels = self.labels.copy()
        new_network.edges = self.edges.copy()
        return new_network

    # ======= # 
    # setters #
    # ======= # 

    def add_node(self, node : int, label : str) -> None:
        """
        add a node to the network with label
        """
        self.nodes.append(node)
        self.edges[node] = {node: 0}
        self.labels[node] = label

    def add_edge(self, node1 : int, node2 : int, duration_bound : float) -> None:
        """
        add an edge to the network with duration bound.
        update the duration bound only if tighter than the current one.
        """
        if node1 not in self.edges:
            self.edges[node1] = {}
        if node2 not in self.edges[node1]:
            self.edges[node1][node2] = duration_bound
        elif duration_bound < self.edges[node1][node2]:
            self.edges[node1][node2] = duration_bound

    def floyd_warshall(self) -> bool:
        """
        use Floyd-Warshall to put the graph in all-pairs shortest path form.
        returns True if the network is temporally consistent (no negative cycles)
        """
        # initialize missing edges 
        for node1 in self.nodes:
            for node2 in self.nodes:
                if node1 != node2 and node2 not in self.edges[node1]:
                    self.edges[node1][node2] = float("inf")
        # run Floyd-Warshall
        for k in self.nodes:
            for i in self.nodes:
                for j in self.nodes:
                    self.edges[i][j] = min(self.edges[i][j], self.edges[i][k] + self.edges[k][j])
                    # check for negative cycles
                    if i==j and self.edges[i][j] < 0:
                        return False
        return True

    def find_shortest_path(self, source : int, sink : int) -> float:
        """
        find the shortest path using dijkstras search
        """
        distances = dict.fromkeys(self.nodes, float("inf"))
        distances[source] = 0
        queue = PriorityQueue()
        visited = set()
        queue.put((0, source))
        while not queue.empty():
            distance, node = queue.get()
            if node == sink: return distance
            if node in visited: continue
            visited.add(node)
            if node not in self.edges: continue
            for neighbor in self.edges[node]:
                if neighbor in visited: continue
                if distances[node] + self.edges[node][neighbor] < distances[neighbor]:
                    distances[neighbor] = distances[node] + self.edges[node][neighbor]
                    queue.put((distances[neighbor], neighbor))
        return float("inf")

    def make_minimal(self):
        """
        removes redundant edges from the network, assuming that the
        network is temporally consistent and already in all-pairs
        shortest path form.
        Reference:
        Nicola Muscettola, Paul Morris, and Ioannis Tsamardinos;
        "Reformulating Temporal Plans For Efficient Execution";
        In Principles of Knowledge Representation and Reasoning (1998).
        """
        for k in self.nodes:
            for i in self.nodes:
                if i == k: continue
                if k not in self.edges[i]: continue
                for j in self.nodes:
                    if i == j or j == k: continue
                    if j not in self.edges[k]: continue
                    if j not in self.edges[i]: continue
                    if self.edges[i][j] < self.edges[i][k] + self.edges[k][j]: continue
                    if self.edges[i][j] < 0 and self.edges[i][k] < 0:
                        del self.edges[i][j]
                    elif self.edges[i][j] >=0 and self.edges[k][j] >= 0:
                        del self.edges[i][j]

    # ======== #
    # printing #
    # ======== #

    def print_dot_graph(self):
        """
        print the graph in DOT format.
        """
        print("digraph G {")
        # declare nodes
        for node in self.nodes:
            print("\t" + str(node) + " [label=\"" + self.labels[node] + "\"];")
        # declare edges
        for node1 in self.nodes:
            for node2 in self.edges[node1]:
                if node1 == node2: continue
                if self.edges[node1][node2] == float("inf"): continue
                print("\t{} -> {} [label=\"{}\"];".format(node1, node2, self.edges[node1][node2]))
        print("}")

    def print_graph_as_json(self):
        """
        print the graph in JSON format.
        """
        print("{")
        print("\t\"nodes\": [")
        for node in self.nodes:
            print("\t\t{\"id\": " + str(node) + ", \"label\": \"" + self.labels[node] + "\"},")
        print("\t],")
        print("\t\"edges\": [")
        for node1 in self.nodes:
            for node2 in self.edges[node1]:
                if node1 == node2: continue
                if self.edges[node1][node2] == float("inf"): continue
                print("\t\t{\"source\": " + str(node1) + ", \"target\": " + str(node2) + ", \"label\": \"" + str(self.edges[node1][node2]) + "\"},")
        print("\t]")
        print("}")