from queue import PriorityQueue
import json
from xmlrpc.client import Boolean
import copy
from math import inf

class TimePoint:
    """
    represents a time point (vertex in the temporal network)
    """
    def __init__(self, id: int, label: str, controllable: bool = True) -> None:
        # controllable: True if time-point can be scheduled, 
        #               False if it cannot (follows an uncertain duration)
        #               Always True for STN
        self.id = id
        self.label = label
        self.controllable = controllable

    def set_controllable(self, logic: bool):
        """
        sets controllable logic of the time-point
        """
        self.controllable = logic
    
    def is_controllable(self) -> bool:
        """
        returns True if time-point is controllable, else False
        """
        if self.controllable == True:
            return True
        else:
            return False
    
    def copy(self):
        """
        returns a copy of the time-point
        """
        return TimePoint(self.id, self.label[:])

    
    def __str__(self) -> str:
        """
        prints string representation of time-point
        """
        return "Time-point {}".format(self.id)
    
    def for_json(self) -> str:
        """
        prints the time-point as a dictionary for use with json
        """
        return {"id": str(self.id), "label": self.label}

class Constraint:
    """
    represents a temporal network constraint (edge in the network)
    """
    def __init__(self, label: str, source: TimePoint, sink: TimePoint, type: str, duration_bound: dict[str, str], distribution: dict[str, str] = None):
        self.label = label
        self.source = source
        self.sink = sink
        assert type in ("stc, pstc"), "Invalid Constraint type, type must be 'stc' for simple temporal constraint, 'stcu' for simple temporal constraint with uncertainty or 'pstc' for probabilistic simple temporal constraint"
        self.type = type
        assert duration_bound.keys() == ["lb", "ub"],  "Duration_bound should be in the form {'lb: float, 'ub': float}"
        self.duration_bound = duration_bound
        assert distribution.keys() == ["mean", "sd"],  "Distribution should be in the form {'mean': float, 'sd': float}"
        self.distribution = distribution
        
    def get_description(self) -> str:
        """
        returns a string of the from c(source.id, sink.id)
        """
        return "c({},{})".format(str(self.source.id), str(self.sink.id))
    
    def copy_constraint(self):
        """
        returns a copy of the constraint
        """
        return Constraint(self.label[:], self.source.copy(), self.sink.copy(), self.type[:], copy.deepcopy(self.duration_bound), distribution = copy.deepcopy(self.distribution))
    
    def set_type(self, type: str) -> None:
        """
        used to change the type of the constraint from stc to pstc or vis versa
        """
        assert type in ("stc, pstc"), "Invalid Constraint type, type must be 'stc' for simple temporal constraint, 'stcu' for simple temporal constraint with uncertainty or 'pstc' for probabilistic simple temporal constraint"
        self.type = type
    
    def set_distribution(self, distribution: dict[str, str]) -> None:
        """
        used to change the distribution of the edge if probabilistic
        """
        if self.type == "pstc":
            assert distribution.keys() == ["mean", "sd"],  "Distribution should be in the form {'mean': float, 'sd': float}"
            self.distribuion = distribution
        else:
            raise AttributeError("Constraint is not of type pstc. Please use constraint.set_type('pstc') first if you wish to change it")
    
    def __str__(self) -> None:
        """
        used to print the constraint in a user-friendly way
        """
        if self.type == "stc":
            return self.get_description() + ": " + "[{}, {}] ".format(self.duration_bound["lb"], self.duration_bound["ub"])
        elif self.type == "pstc":
            return self.get_description() + ": " + "N({}, {})".format(self.distribution["mean"], self.distribution["variance"])

    def for_json(self) -> dict:
        """
        returns the constraint as a dictionary for use with json
        """
        to_return = {"source": self.source.id, "sink": self.sink.id, "label": self.label, "type": self.type, "duration_bound": {"lb": self.lb, "ub": self.lb}}
        if self.type == "pstc":
            to_return["distribution"] = {"mean": self.mean, "sd": self.sd}
        return to_return

    @property
    def mean(self):
        if self.distribution != None:    
            return self.distribution["mean"]
        else:
            raise ValueError("Constraint is not probabilistic and so has no mean")

    @property
    def sd(self):
        if self.distribution != None:    
            return self.distribution["sd"]
        else:
            raise ValueError("Constraint is not probabilistic and so has no standard deviation")
    
    @property
    def lb(self):
        return self.duration_bound["lb"]

    @property
    def ub(self):
        return self.duration_bound["ub"]

class TemporalNetwork:
    """
    represents a simple temporal network as a graph.
    """
    def __init__(self, name: str) -> None:
        self.name = name
        self.time_points : list[TimePoint] = []
        self.constraints: list[Constraint] = []

    def add_time_point(self, time_point: TimePoint) -> None:
        """
        add a time-point (node) to the network.
        """
        self.time_points.append(time_point)


    def add_constraint(self, constraint: Constraint) -> None:
        """
        add an edge (constraint) to the network. only constraints of type 'stc' are permitted in Temporal Network.
        """
        assert constraint.type == "stc", "Only time-points of the type 'stc' are permitted."
        self.constraints.append(constraint)
    
    def get_adjacency_matrix(self) -> dict[TimePoint, dict]:
        """
        gets adjacency matrix (dictionary) representation of temporal-network
        """
        adj = {}
        # Initialises adj matrix using edges explicit in self.constraints
        for constraint in self.constraints:
            # If source not in adj matrix yet, add it
            if str(constraint.source.id) not in adj:
                adj[str(constraint.source.id)] = {}
            # If sink not in adj matrix yet, add it
            if str(constraint.sink.id) not in adj:
                adj[str(constraint.sink.id)] = {}
            # If source[sink] not in adj matrix yet, add it.
            if str(constraint.sink.id) not in adj[str(constraint.source.id)]:
                adj[str(constraint.source.id)][str(constraint.sink.id)] = constraint.ub
            # If sink[source] not in adj matrix yet, add it
            if str(constraint.source.id) not in adj[str(constraint.sink.id)]:
                adj[str(constraint.sink.id)][str(constraint.source.id)] = -constraint.lb
        
        # Adds self edges to be equal to zero and initialises missing edges to be infinity
        for node1 in self.time_points:
            if str(node1.id) not in adj:
                adj[str(node1.id)] = {}
            for node2 in self.time_points:
                if node1 == node2:
                    adj[str(node1.id)][str(node2.id)] = 0
                elif str(node2.id) not in adj[str(node1.id)]:
                    adj[str(node1.id)][str(node2.id)] = inf
        return adj

    def floyd_warshall(self) -> tuple(dict[TimePoint], bool):
        """
        use Floyd-Warshall to put the graph in all-pairs shortest path form.
        returns tuple (APSP dictionary, boolean) where the boolean is True if the network is consistent (i.e. no negative cycles).
        """
        adj = self.get_adjacency_matrix()

        # run Floyd-Warshall
        for k in adj:
            for i in adj:
                for j in adj:
                    adj[i][j] = min(adj[i][j], adj[i][k] + adj[k][j])
                    # check for negative cycles
                    if i==j and adj[i][j] < 0:
                        return (adj, False)
        return (adj, True)

    def find_shortest_path(self, source : int, sink : int) -> float:
        """
        find the shortest path using dijkstras search
        """
        # Needs updated
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

    def make_minimal(self) -> dict[TimePoint]:
        """
        removes redundant edges from the network, assuming that the
        network is temporally consistent and already in all-pairs
        shortest path form.
        Reference:
        Nicola Muscettola, Paul Morris, and Ioannis Tsamardinos;
        "Reformulating Temporal Plans For Efficient Execution";
        In Principles of Knowledge Representation and Reasoning (1998).
        """
        check = self.floyd_warshall()
        adj, consistent = check[0], check[1]
        if consistent == False:
            raise AttributeError("Network is not consistent")    
        for k in adj:
            for i in adj:
                if i == k: continue
                if k not in adj[i]: continue
                for j in adj:
                    if i == j or j == k: continue
                    if j not in adj[k]: continue
                    if j not in adj[i]: continue
                    if adj[i][j] < adj[i][k] + adj[k][j]: continue
                    if adj[i][j] < 0 and adj[i][k] < 0:
                        del adj[i][j]
                    elif adj[i][j] >=0 and adj[k][j] >= 0:
                        del adj[i][j]
        return adj
    
    def get_outgoing_edge(self, constraint: Constraint) -> list[Constraint]:
        """
        given an edge (i, j), returns a list of outgoing edges (j, k)
        """
        return [jk for jk in self.constraints if jk.source == constraint.sink]
    
    def get_incoming_edge(self, constraint: Constraint) -> list[Constraint]:
        """
        given an edge (j, k), returns a list of incoming edges (i, j)
        """
        return [ij for ij in self.constraints if ij.sink == constraint.source]
    
    def get_constraint_by_timepoint(self, source: TimePoint, sink: TimePoint) -> Constraint:
        """
        given two time-points, i and j, if a constraint exists between the two it returns the constraint, else raises exception 
        """
        for constraint in self.constraints:
            if constraint.source == source and constraint.sink == sink:
                return constraint
            elif constraint.sink == source and constraint.source == sink:
                return constraint
            else:
                raise AttributeError("No constraint between the two time-points")
                        
    def print_dot_graph(self):
        """
        print the graph in DOT format.
        """
        print("digraph G {")
        # declare nodes
        for time_point in self.time_points:
            print("\t" + str(time_point.id) + " [label=\"" + time_point.label + "\"];")
        # declare edges
        for constraint in self.constraints:
            print("\t{} -> {} [label=\"({},{})\"];".format(constraint.source, constraint.sink, constraint.lb, constraint.ub))
        print("}")

    def print_graph_as_json(self):
        """
        print the graph in JSON format.
        """
        print("{")
        print("\t\"timepoints\": [")
        for time_point in self.time_points:
            print("\t\t{\"id\": " + str(time_point.id) + ", \"label\": \"" + time_point.label + "\"},")
        print("\t],")
        print("\t\"constraints\": [")
        for constraint in self.constraints:
            print("\t\t{\"source\": " + str(constraint.source.id) + ", \"target\": " + str(constraint.sink.id) + ", \"label\": \"" + "({}.{})".format(constraint.lb, constraint.ub) + "\"},")
        print("\t]")
        print("}")
    
    def save_as_json(self, filename):
        """
        Saves the network as a JSON to filename.json
        """
        toDump = {}
        toDump["timepoints"] = [t.for_json() for t in self.time_points]
        toDump["constraints"] = [c.for_json() for c in self.constraints]
        with open("{}.json".format(filename), 'w') as fp:
            json.dump(toDump, fp)

