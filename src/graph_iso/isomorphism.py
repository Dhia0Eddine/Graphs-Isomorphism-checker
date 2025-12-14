""" isomorphis checker for graphs
    it works by backtracking through all possible mappings
    of nodes from one graph to another according to their degrees starting form the lowest degree nodes
    if a valid mapping is found that preserves adjacency, the graphs are isomorphic
"""

class IsomorphismChecker:
    def __init__(self, graph1, graph2):
        self.graph1 = graph1
        self.graph2 = graph2

    def are_isomorphic(self):
        nodes1 = self.graph1.get_nodes()
        nodes2 = self.graph2.get_nodes()

        if len(nodes1) != len(nodes2): #  they cant be isomorphic if they have different number of nodes
            return False


        degree_map1 = self.graph1.get_degree_mapping() # this will map degree to list of nodes with that degree in graph1
        degree_map2 = self.graph2.get_degree_mapping() # this will map degree to list of nodes with that degree in graph2

        if sorted(degree_map1.keys()) != sorted(degree_map2.keys()): # necessary condition: both graphs must have same degree sequence
            return False

        for degree in degree_map1:
            if len(degree_map1[degree]) != len(degree_map2[degree]): # necessary condition: same number of nodes with same degree
                return False

        mapping = {} # node from graph1 to node from graph2
        used = set() # nodes in graph2 that are already mapped
        

        """
        recursive backtracking function to find valid mapping
        it works by assuming a mapping for the current node and checking if it leads to a valid solution
        if not, it backtracks and tries the next possible mapping
        and so on until all nodes are processed
        if a valid mapping is found, it returns True
        else, it returns False
        it takes the current index of node in nodes1 to process 

        """

        def backtrack(index):
            if index == len(nodes1): #  this is the base case, all nodes have been processed
                return True

            current_node = nodes1[index]
            current_degree = self.graph1.get_degree(current_node)
            possible_nodes = degree_map2[current_degree] # get nodes in graph2 with same degree as current_node

            for candidate in possible_nodes:
                if candidate in used:
                    continue

                # assume mapping
                mapping[current_node] = candidate
                used.add(candidate)

                if self.is_valid_mapping(mapping):
                    if backtrack(index + 1):
                        return True
                


                # backtrack
                del mapping[current_node] # remove the assumed mapping
                used.remove(candidate) # mark candidate as unused for future mappings

                return False
            
        return backtrack(0) # start backtracking from the first node, this will initiate the backtracking process in the isomorphism checker
            
               
    def is_valid_mapping(self, mapping): # this function checks if the current mapping preserves adjacency,
        for u in mapping: # for each mapped node in graph1, mapping is of the form {node_in_graph1: node_in_graph2} so u will hold tha value of node_in_graph1
            mapped_u = mapping[u] # get the corresponding node in graph2
            for v in self.graph1.get_neighbors(u): # for each neighbor of u in graph1
                if v in mapping: # if the neighbor is also mapped which means we have a mapping for it
                    mapped_v = mapping[v] # get the corresponding node in graph2 of neighbor v
                    if mapped_v not in self.graph2.get_neighbors(mapped_u): # check if mapped_v is a neighbor of mapped_u in graph2, this checks if adjacency is preserved for this pair of nodes
                        return False
        return True
    