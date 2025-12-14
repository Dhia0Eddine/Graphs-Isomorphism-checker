# this is a graph class implementation using adjacency list representation

class Graph:
    def __init__(self):
        """
        dictionary to hold adjacency list
        ,each key is a node and value is a list of connected nodes
        """

        self.adjacency_list = {} 

    def add_edge(self, u, v):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)  # For undirected graph

    def remove_edge(self, u, v):
        if u in self.adjacency_list and v in self.adjacency_list[u]:
            self.adjacency_list[u].remove(v)
        if v in self.adjacency_list and u in self.adjacency_list[v]:
            self.adjacency_list[v].remove(u)

    def get_neighbors(self, u):
        return self.adjacency_list.get(u, [])
    
    def get_nodes(self):
        return list(self.adjacency_list.keys())
    
    def get_degree(self, u):
        return len(self.adjacency_list.get(u, []))
    def get_degree_mapping(self):
        degree_map = {}
        for node in self.get_nodes():
            degree = self.get_degree(node)
            if degree not in degree_map:
                degree_map[degree] = []
            degree_map[degree].append(node)
        return degree_map
    def __str__(self):
        return str(self.adjacency_list)
    
 