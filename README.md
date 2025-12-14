Graphs Isomorphism Checker
==========================

An educational toolkit for experimenting with graph isomorphism. It provides:

- A lightweight `Graph` data structure with JSON parsing utilities.
- A backtracking-based `IsomorphismChecker` that can emit detailed trace data.
- A Tkinter-driven visual debug experience that highlights the current/visited/rejected nodes in two graphs and lets you step through the solver using the Enter key.
- Notebook and script examples that show how to load sample graphs and launch the interactive explorer.

Getting Started
---------------

### 1. Clone and install

```
git clone https://github.com/Dhia0Eddine/Graphs-Isomorphism-checker.git
cd Graphs Isomorphism checker
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pip install -r requirements.txt
```

The editable install (`-e .`) registers the `graph_iso` package so you can run the examples and notebooks without fiddling with `PYTHONPATH`.

### 2. Run the interactive visualizer

```
python examples/interactive_visualizer.py
```

The script loads `data/sample_graphs.json`, computes the solver trace, and opens a pop-up window. Use the *Next step* button or press **Enter** to advance. Each step shows:

- Current node under consideration (orange) and visited nodes (green) in Graph 1.
- Candidate, accepted, and rejected nodes in Graph 2 (purple / green / red).
- A textual summary of the solver event plus the current mapping list.

### 3. Notebook workflow (optional)

Open `notebooks/graph_analysis.ipynb`, run the cells in order, and the final cell will launch the same Tkinter window. This is useful if you want to tweak the graphs interactively in a Jupyter session but still inspect the search visually outside the notebook.

Project Structure
-----------------

- `src/graph_iso/graph.py` – Adjacency-list graph implementation.
- `src/graph_iso/parser.py` – JSON graph loader for single or multiple graphs.
- `src/graph_iso/isomorphism.py` – Backtracking isomorphism solver with trace emission helpers.
- `src/graph_iso/visualization.py` – Tkinter-based stepper used by both the notebook and CLI example.
- `examples/interactive_visualizer.py` – Command-line entry point that wires the parser, solver, and visualizer.
- `data/sample_graphs.json` – Example graphs used by the demos/tests.
- `tests/` – Pytest-based sanity checks for the graph and solver primitives.

Algorithm Explanation
---------------------

1. **Pre-check filters**
	- Compare node counts. If the graphs have different sizes, they cannot be isomorphic.
	- Build degree mappings (`degree -> [nodes]`) for both graphs. The checker rejects pairs that do not have identical degree sequences or counts per degree class.

2. **Backtracking search**
	- Order nodes from `graph1` (current implementation keeps the insertion order returned by the adjacency list).
	- For the node at position `index`, pick the candidate set of nodes in `graph2` that share the same degree. Track used nodes to avoid duplicates.
	- Tentatively map `graph1[index] -> candidate`, append to the `mapping`, and validate the partial assignment.

3. **Adjacency validation**
	- Every time a new pair is assumed, `is_valid_mapping()` ensures that all already-mapped neighbors preserve adjacency: if `u` connects to `v` in `graph1`, the mapped nodes must also connect in `graph2`.
	- If the check fails, the candidate is marked as rejected for the current node and removed from the mapping.

4. **Trace emission**
	- The solver accepts an optional `trace_callback` invoked with structured events (`select_node`, `try_candidate`, `reject_candidate`, `backtrack`, `complete`, etc.).
	- `trace_states()` wraps the solver, collects the stream into a list, and returns `(result, timeline)` for consumers such as the GUI.

5. **Visualization layer**
	- `GraphVisualizer` replays the timeline in a Tkinter window, highlighting the current node, visited nodes, and rejected candidates while printing the textual event summary and the current mapping.

Complexity Overview
-------------------

| Scenario | Nodes (`n`) | Edges (`m`) | Worst-case time | Space |
| --- | --- | --- | --- | --- |
| Dense graphs with no pruning | `n` | `O(n^2)` | `O(n!)` – the solver may explore every permutation of node mappings before concluding | `O(n)` for mapping + call stack |
| Sparse graphs with degree filters | `n` | `O(n)` | `O(k^n)` where `k` is the maximum number of candidates per degree class (often far smaller than `n` in practice) | `O(n)` |
| Early mismatch detected by pre-checks | `n` | any | `O(n + m)` – building degree maps and noticing the mismatch stops the search | `O(n)` |

> **Note:** Graph isomorphism is neither known to be polynomial nor proven NP-complete. A naive backtracking approach like this one has factorial worst-case behavior, but the degree constraints and adjacency checks dramatically prune the search tree for most practical inputs.

Custom Data
-----------

To visualize your own graphs, update `data/sample_graphs.json` or point the parser to a different file inside `examples/interactive_visualizer.py`. Each graph entry should contain an `"edges"` list of two-element arrays, e.g.:

```
{
	"graph1": {"edges": [["A", "B"], ["B", "C"]]},
	"graph2": {"edges": [["X", "Y"], ["Y", "Z"]]}
}
```

Testing
-------

```
python -m pytest
```

