# parser for the application it is used ot parse input files and create graph objectsimport json
from .graph import Graph  # import your Graph class
import json

class GraphParser:
    def __init__(self, file_path):
        self.file_path = file_path
    
    """Class to parse graph data from JSON files."""
    def load_graph_from_json(self):
        """Load a single graph from a JSON file."""
        with open(self.file_path) as f:
            data = json.load(f)
        
        g = Graph()
        for u, v in data["edges"]:
            g.add_edge(u, v)
        return g

    def load_multiple_graphs(self, file_path):
        """Load multiple graphs from a JSON file containing several graphs."""
        with open(self.file_path) as f:
            data = json.load(f)
        
        graphs = {}
        for graph_name, graph_data in data.items():
            g = Graph()
            for u, v in graph_data["edges"]:
                g.add_edge(u, v)
            graphs[graph_name] = g
        return graphs
