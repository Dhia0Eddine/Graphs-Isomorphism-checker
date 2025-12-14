"""Launch the interactive graph isomorphism visualization GUI."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from graph_iso.isomorphism import IsomorphismChecker
from graph_iso.parser import GraphParser
from graph_iso.visualization import GraphVisualizer


def main():
    data_path = ROOT / "data" / "sample_graphs.json"
    graphs = GraphParser(str(data_path)).load_multiple_graphs()
    graph1 = graphs["graph1"]
    graph2 = graphs["graph2"]

    checker = IsomorphismChecker(graph1=graph1, graph2=graph2)
    result, trace_states = checker.trace_states()
    print(f"Are graphs isomorphic? {result}")
    print(f"Recorded {len(trace_states)} tracing steps.")

    visualizer = GraphVisualizer(graph1, graph2, trace_states)
    visualizer.run()


if __name__ == "__main__":
    main()
