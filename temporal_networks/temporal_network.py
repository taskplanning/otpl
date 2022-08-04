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
    
    def to_json(self) -> str:
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
        assert list(duration_bound.keys()) == ["lb", "ub"],  "Duration_bound should be in the form {'lb: float, 'ub': float}"
        self.duration_bound = duration_bound
        if distribution != None:
            assert list(distribution.keys()) == ["mean", "sd"],  "Distribution should be in the form {'mean': float, 'sd': float}"
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

    def to_json(self) -> dict:
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
    def __init__(self) -> None:
        self.name = None
        self.time_points : list[TimePoint] = []
        self.constraints: list[Constraint] = []
    
    def copy(self):
        return TemporalNetwork(self.name, copy.deepcopy(self.time_points), copy.deepcopy(self.constraints))

    def add_time_point(self, time_point: TimePoint) -> None:
        """
        add a time-point (node) to the network.
        """
        for t in self.time_points:
            if t.id == time_point.id:
                raise ValueError("Time-point already exists in network with that ID. Try changing ID of new time-point so that it is unique.")
        self.time_points.append(time_point)
    
    def add_name(self, name: str) -> None:
        """
        adds a string name to the network.
        """
        self.name = name

    def add_constraint(self, constraint: Constraint) -> None:
        """
        add an edge (constraint) to the network. only constraints of type 'stc' are permitted in Temporal Network.
        if source and sink nodes not in the time_points set, it adds them
        """
        assert constraint.type == "stc", "Only time-points of the type 'stc' are permitted."
        # Checks if there is already a constraint with those time-points, if not it adds
        existing = self.get_constraint_by_timepoint(constraint.source, constraint.sink)
        if existing == None:
            self.constraints.append(constraint)
            if constraint.source not in self.time_points:
                self.add_time_point(constraint.source)
            if constraint.sink not in self.time_points:
                self.add_time_point(constraint.sink)
        # If the source and sink time-points are the same way round in the new constraint versus existing
        elif existing.source == constraint.source:
            # Checks whether the new constraint has a tighter bound
            if constraint.ub < existing.ub:
                existing.ub = constraint.ub
            elif constraint.lb > existing.lb:
                existing.lb = constraint.lb
        # If the source and sink time-points are the wrong way round in the new constraint versus existing
        elif existing.sink == constraint.source:
            if -constraint.lb < existing.ub:
                existing.ub = -constraint.lb
            if -constraint.ub > existing.lb:
                existing.lb = -constraint.ub

    def get_adjacency_matrix(self) -> dict[TimePoint, dict]:
        """
        gets adjacency matrix (dictionary) representation of temporal-network
        """
        adj = {}
        # Initialises adj matrix using edges explicit in self.constraints
        for constraint in self.constraints:
            # If source not in adj matrix yet, add it
            if constraint.source.id not in adj:
                adj[constraint.source.id] = {}
            # If sink not in adj matrix yet, add it
            if constraint.sink.id not in adj:
                adj[constraint.sink.id] = {}
            # If source[sink] not in adj matrix yet, add it.
            if constraint.sink.id not in adj[constraint.source.id]:
                adj[constraint.source.id][constraint.sink.id] = constraint.ub
            # If sink[source] not in adj matrix yet, add it
            if constraint.source.id not in adj[constraint.sink.id]:
                adj[constraint.sink.id][constraint.source.id] = -constraint.lb
        
        # Adds self edges to be equal to zero and initialises missing edges to be infinity
        for node1 in self.time_points:
            if node1.id not in adj:
                adj[node1.id] = {}
            for node2 in self.time_points:
                if node1 == node2:
                    adj[node1.id][node2.id] = 0
                elif node2.id not in adj[node1.id]:
                    adj[node1.id][node2.id] = inf
        return adj
    
    def get_bidirectional_network(self) -> dict[TimePoint, dict]:
        """
        Gets the bidirectional version of the temporal network, i.e. converts from l12 <= b2 - b1 <= u12 to b2 - b1 <= u12, b1 - b2 <= -l12
        As above but does not consider all pairs.
        """
        network = {}
        for constraint in self.constraints:
            # If source not in adj matrix yet, add it
            if constraint.source.id not in network:
                network[constraint.source.id] = {}
            # If sink not in adj matrix yet, add it
            if constraint.sink.id not in network:
                network[constraint.sink.id] = {}
            # If source[sink] not in adj matrix yet, add it.
            if constraint.sink.id not in network[constraint.source.id]:
                network[constraint.source.id][constraint.sink.id] = constraint.ub
            # If sink[source] not in adj matrix yet, add it
            if constraint.source.id not in network[constraint.sink.id]:
                network[constraint.sink.id][constraint.source.id] = -constraint.lb
        return network


    def floyd_warshall(self) -> tuple[dict[TimePoint, dict], bool]:
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
        network = self.get_bidirectional_network()
        distances = dict.fromkeys([i.id for i in self.time_points], float("inf"))
        distances[source.id] = 0
        queue = PriorityQueue()
        visited = set()
        queue.put((0, source))
        while not queue.empty():
            distance, node = queue.get()
            if node == sink: return distance
            if node in visited: continue
            visited.add(node)
            if node not in network: continue
            for neighbor in network[node]:
                if neighbor in visited: continue
                if distances[node] + network[node][neighbor] < distances[neighbor]:
                    distances[neighbor] = distances[node] + network[node][neighbor]
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
                return None

    def get_timepoint_by_id(self, id: int) -> TimePoint:
        """
        given an id, it returns the time-point if it exists in self.timepoints
        """
        found = None
        for time_point in self.time_points:
            if time_point.id == id:
                found = time_point
        return found
            
                        
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
            print("\t\t{\"source\": " + str(constraint.source.id) + ", \"target\": " + str(constraint.sink.id) + ", \"label\": \"" + "({}, {})".format(constraint.lb, constraint.ub) + "\"},")
        print("\t]")
        print("}")
    
    def save_as_json(self, filename):
        """
        saves the network as a JSON to filename.json
        """
        toDump = {}
        toDump["timepoints"] = [t.to_json() for t in self.time_points]
        toDump["constraints"] = [c.to_json() for c in self.constraints]
        with open("{}.json".format(filename), 'w') as fp:
            json.dump(toDump, fp)


class ProbabilisticTemporalNetwork(TemporalNetwork):
    """
    represents a probabilistic temporal network.
    """
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def adds_constraint(self, constraint: Constraint) -> None:
        """
        add an edge (constraint) to the network. permits constraints of type 'pstc'.
        """
        # Checks if there is already a constraint with those time-points, if not it adds
        existing = self.get_constraint_by_timepoint(constraint.source, constraint.sink)
        if existing == None:
            self.constraints.append(constraint)
            if constraint.source not in self.time_points:
                self.add_time_point(constraint.source)
            if constraint.sink not in self.time_points:
                self.add_time_point(constraint.sink)
        # If the source and sink time-points are the same way round in the new constraint versus existing
        elif existing.source == constraint.source:
            # Checks whether the new constraint has a tighter bound
            if constraint.ub < existing.ub:
                existing.ub = constraint.ub
            elif constraint.lb > existing.lb:
                existing.lb = constraint.lb
        # If the source and sink time-points are the wrong way round in the new constraint versus existing
        elif existing.sink == constraint.source:
            if -constraint.lb < existing.ub:
                existing.ub = -constraint.lb
            if -constraint.ub > existing.lb:
                existing.lb = -constraint.ub
    
    def get_probabilistic_constraints(self) -> list[Constraint]:
        """
        returns a list of probabilistic constraints (those with type = pstc)
        """
        return [i for i in self.constraints if i.type == "pstc"]

    
    def get_requirement_constraints(self) -> list[Constraint]:
        """
        returns a list of requirement constraints (those with type = stc)
        """
        return [i for i in self.constraints if i.type == "stc"]

    def set_controllability_of_time_points(self) -> None:
        """
        checks which time_points are uncontrollable (i.e. they come at the end of a probabilistic constraint). Sets the controllable flag
        to True if controllable and False if not controllable
        """
        uncontrollable_time_points = [i.sink for i in self.get_probabilistic_constraints()]
        for time_point in self.time_points:
            if time_point in uncontrollable_time_points:
                time_point.set_controllable("False")
            else:
                time_point.set_controllable("True")
    
    def get_controllable_time_points(self) -> list[TimePoint]:
        """
        returns a list of controllable time-points
        """
        self.set_controllability_of_time_points()
        return [i for i in self.time_points if i.is_controllable == True]
    
    def get_uncontrollable_time_points(self) -> list[TimePoint]:
        """
        returns a list of uncontrollable time-points
        """
        self.set_controllability_of_time_points()
        return [i for i in self.time_points if i.is_controllable == False]
    
    def get_uncontrollable_constraints(self) -> list[Constraint]:
        """
        returns a list of requirement constraints that contain an uncontrollable time-point
        """
        self.set_controllability_of_time_points()
        uncontrollable_constraints = []
        for constraint in self.constraints:
            if constraint.source.is_controllable() == False or constraint.sink.is_controllable() == False:
                uncontrollable_constraints.append(constraint)
    
    def incoming_probabilistic(self, constraint) -> dict[str, Constraint]:
        """
        returns a dictionary of the incoming probabilistic constraint in the form {"start": Constraint, "end": Constraint}
        raises an exception if the number of incoming probabilistic constraints is greater than one
        """
        if constraint not in self.get_uncontrollable_constraints():
            return None
        else:
            incoming_source = [g for g in self.getContingents() if g.sink == constraint.source]
            incoming_sink = [g for g in self.getContingents() if g.sink == constraint.sink]
            if len(incoming_source) > 1 or len(incoming_sink) > 1:
                raise AttributeError("More than one incoming probabilistic edge.")
            else:
                try:
                    return {"start": incoming_source[0], "end": incoming_sink[0]}
                except IndexError:
                    try:
                        return {"start": incoming_source[0], "end": None}
                    except IndexError:
                        return {"start": None, "end": incoming_sink[0]}


    
