""" isomorphis checker for graphs
    it works by backtracking through all possible mappings
    of nodes from one graph to another according to their degrees starting form the lowest degree nodes
    if a valid mapping is found that preserves adjacency, the graphs are isomorphic
"""

class IsomorphismChecker:
    def __init__(self, graph1, graph2):
        self.graph1 = graph1
        self.graph2 = graph2

    def are_isomorphic(self, trace_callback=None):
        nodes1 = self.graph1.get_nodes()
        nodes2 = self.graph2.get_nodes()

        mapping = {}  # node from graph1 to node from graph2
        used = set()  # nodes in graph2 that are already mapped
        rejection_tracker = {}  # records rejected candidates per node for tracing

        step_counter = {"value": 0}

        def emit(event, **kwargs):
            if not trace_callback:
                return

            step_counter["value"] += 1
            payload = {
                "step": step_counter["value"],
                "event": event,
                "mapping": dict(mapping),
                "used_nodes": sorted(list(used)),
                "current_node": kwargs.get("current_node"),
                "candidate": kwargs.get("candidate"),
                "rejected_candidates": sorted(list(kwargs.get("rejected_candidates", []))),
                "message": kwargs.get("message"),
            }
            trace_callback(payload)

        if len(nodes1) != len(nodes2):  # they cant be isomorphic if they have different number of nodes
            emit(
                "precheck_failed",
                message="Graphs have different numbers of nodes, so they cannot be isomorphic.",
            )
            return False

        degree_map1 = self.graph1.get_degree_mapping()  # this will map degree to list of nodes with that degree in graph1
        degree_map2 = self.graph2.get_degree_mapping()  # this will map degree to list of nodes with that degree in graph2

        if sorted(degree_map1.keys()) != sorted(degree_map2.keys()):  # necessary condition: both graphs must have same degree sequence
            emit(
                "precheck_failed",
                message="Graphs have different degree sequences, so they cannot be isomorphic.",
            )
            return False

        for degree in degree_map1:
            if len(degree_map1[degree]) != len(
                degree_map2[degree]
            ):  # necessary condition: same number of nodes with same degree
                emit(
                    "precheck_failed",
                    message=f"Graphs differ in the number of nodes with degree {degree}.",
                )
                return False

        def backtrack(index):
            if index == len(nodes1):  # this is the base case, all nodes have been processed
                emit("complete", message="Isomorphism found. All nodes mapped successfully.")
                return True

            current_node = nodes1[index]
            rejection_tracker[current_node] = set()
            current_degree = self.graph1.get_degree(current_node)
            possible_nodes = degree_map2[current_degree]  # get nodes in graph2 with same degree as current_node

            emit(
                "select_node",
                current_node=current_node,
                rejected_candidates=rejection_tracker[current_node],
                message=f"Selecting node {current_node} for mapping.",
            )

            for candidate in possible_nodes:
                if candidate in used:
                    continue

                # assume mapping
                mapping[current_node] = candidate
                used.add(candidate)
                emit(
                    "try_candidate",
                    current_node=current_node,
                    candidate=candidate,
                    rejected_candidates=rejection_tracker[current_node],
                    message=f"Trying to map {current_node} -> {candidate}.",
                )

                if self.is_valid_mapping(mapping):
                    emit(
                        "partial_valid",
                        current_node=current_node,
                        candidate=candidate,
                        rejected_candidates=rejection_tracker[current_node],
                        message="Partial mapping valid so far.",
                    )
                    if backtrack(index + 1):
                        return True

                rejection_tracker[current_node].add(candidate)
                emit(
                    "reject_candidate",
                    current_node=current_node,
                    candidate=candidate,
                    rejected_candidates=rejection_tracker[current_node],
                    message=f"Mapping {current_node} -> {candidate} rejected.",
                )

                # backtrack
                del mapping[current_node]  # remove the assumed mapping
                used.remove(candidate)  # mark candidate as unused for future mappings

            emit(
                "backtrack",
                current_node=current_node,
                rejected_candidates=rejection_tracker[current_node],
                message=f"Backtracking from node {current_node}.",
            )
            return False

        result = backtrack(0)  # start backtracking from the first node

        if not result:
            emit("failure", message="No isomorphism found after exploring all mappings.")

        return result
            
               
    def trace_states(self):
        """Run the isomorphism check while recording each decision step."""

        timeline = []

        def recorder(state):
            # make a shallow copy of the state so downstream consumers can mutate safely
            timeline.append(dict(state))

        result = self.are_isomorphic(trace_callback=recorder)
        return result, timeline

    def is_valid_mapping(self, mapping): # this function checks if the current mapping preserves adjacency,
        for u in mapping: # for each mapped node in graph1, mapping is of the form {node_in_graph1: node_in_graph2} so u will hold tha value of node_in_graph1
            mapped_u = mapping[u] # get the corresponding node in graph2
            for v in self.graph1.get_neighbors(u): # for each neighbor of u in graph1
                if v in mapping: # if the neighbor is also mapped which means we have a mapping for it
                    mapped_v = mapping[v] # get the corresponding node in graph2 of neighbor v
                    if mapped_v not in self.graph2.get_neighbors(mapped_u): # check if mapped_v is a neighbor of mapped_u in graph2, this checks if adjacency is preserved for this pair of nodes
                        return False
        return True
    