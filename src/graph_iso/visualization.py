"""Interactive visualization helpers for graph isomorphism traces."""

from __future__ import annotations

import math
import tkinter as tk
from typing import Dict, Iterable, List, Tuple

NodePositions = Dict[str, Tuple[float, float]]
TraceState = Dict[str, object]

NODE_RADIUS = 26
CANVAS_SIZE = (420, 420)
BACKGROUND_COLOR = "#f5f5f5"
EDGE_COLOR = "#90a4ae"
OUTLINE_COLOR = "#263238"


class GraphVisualizer:
    """Tkinter-based stepper that replays isomorphism search traces."""

    def __init__(self, graph1, graph2, trace_states: Iterable[TraceState]):
        self.graph1 = graph1
        self.graph2 = graph2
        self.trace_states: List[TraceState] = list(trace_states)
        if not self.trace_states:
            raise ValueError("trace_states must contain at least one step.")

        self.positions_g1 = self._compute_positions(self.graph1)
        self.positions_g2 = self._compute_positions(self.graph2)

        self.current_index = 0
        self.root = tk.Tk()
        self.root.title("Graph Isomorphism Explorer")
        self.root.configure(bg="white")
        self.root.bind("<Return>", self._handle_enter)

        self.status_var = tk.StringVar()
        self.message_var = tk.StringVar()
        self.mapping_var = tk.StringVar()

        self._build_ui()
        self._render_step()

    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def _build_ui(self):
        header = tk.Label(
            self.root,
            text="Interactively step through the solver. Use the Next button or press Enter.",
            bg="white",
            font=("Segoe UI", 11),
        )
        header.pack(pady=(10, 4))

        status = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="white",
            fg="#37474f",
            font=("Segoe UI", 10, "bold"),
        )
        status.pack()

        graph_frame = tk.Frame(self.root, bg="white")
        graph_frame.pack(pady=10)

        self.canvas_g1 = tk.Canvas(
            graph_frame,
            width=CANVAS_SIZE[0],
            height=CANVAS_SIZE[1],
            bg=BACKGROUND_COLOR,
            highlightthickness=1,
            highlightbackground="#cfd8dc",
        )
        self.canvas_g1.pack(side=tk.LEFT, padx=12)

        self.canvas_g2 = tk.Canvas(
            graph_frame,
            width=CANVAS_SIZE[0],
            height=CANVAS_SIZE[1],
            bg=BACKGROUND_COLOR,
            highlightthickness=1,
            highlightbackground="#cfd8dc",
        )
        self.canvas_g2.pack(side=tk.LEFT, padx=12)

        message_label = tk.Label(
            self.root,
            textvariable=self.message_var,
            bg="white",
            fg="#37474f",
            wraplength=820,
            justify=tk.LEFT,
            font=("Segoe UI", 10),
        )
        message_label.pack(padx=16, pady=(4, 2))

        mapping_title = tk.Label(
            self.root,
            text="Current mapping",
            bg="white",
            fg="#546e7a",
            font=("Segoe UI", 10, "bold"),
        )
        mapping_title.pack(pady=(6, 0))

        mapping_label = tk.Label(
            self.root,
            textvariable=self.mapping_var,
            bg="white",
            fg="#212121",
            font=("Consolas", 10),
            justify=tk.LEFT,
        )
        mapping_label.pack(padx=16, pady=(0, 10))

        controls = tk.Frame(self.root, bg="white")
        controls.pack(pady=(0, 12))

        self.next_button = tk.Button(
            controls,
            text="Next step (Enter)",
            command=self.next_step,
            width=18,
            bg="#1976d2",
            fg="white",
            activebackground="#1565c0",
            activeforeground="white",
            relief=tk.FLAT,
        )
        self.next_button.pack()

    def next_step(self):
        """Advance to the next recorded state."""
        if self.current_index >= len(self.trace_states) - 1:
            self.next_button.configure(state=tk.DISABLED, text="Complete")
            self.status_var.set("Reached final step. Close the window to exit.")
            return

        self.current_index += 1
        self._render_step()

        if self.current_index == len(self.trace_states) - 1:
            self.next_button.configure(text="Finish")

    def _handle_enter(self, _event):
        self.next_step()

    def _render_step(self):
        state = self.trace_states[self.current_index]
        total_steps = len(self.trace_states)
        step_no = state.get("step", self.current_index + 1)
        event = str(state.get("event", ""))
        message = str(state.get("message", ""))
        mapping = state.get("mapping", {}) or {}
        current_node = state.get("current_node")
        candidate = state.get("candidate")
        rejected = set(state.get("rejected_candidates") or [])
        visited_g1 = set(mapping.keys())
        visited_g2 = set(mapping.values())

        self.status_var.set(
            f"Step {step_no} / {total_steps} · {event.replace('_', ' ').title()}"
        )
        self.message_var.set(message)
        self.mapping_var.set(self._format_mapping(mapping))

        self._draw_graph(
            canvas=self.canvas_g1,
            graph=self.graph1,
            positions=self.positions_g1,
            color_fn=lambda node: self._color_graph1(node, current_node, visited_g1),
        )

        self._draw_graph(
            canvas=self.canvas_g2,
            graph=self.graph2,
            positions=self.positions_g2,
            color_fn=lambda node: self._color_graph2(
                node, candidate, visited_g2, rejected
            ),
        )

    def _draw_graph(self, canvas: tk.Canvas, graph, positions: NodePositions, color_fn):
        canvas.delete("all")
        width = int(canvas["width"])
        height = int(canvas["height"])
        scale = min(width, height) / 2 - NODE_RADIUS - 12

        def project(x_val: float, y_val: float) -> Tuple[float, float]:
            return (
                width / 2 + x_val * scale,
                height / 2 - y_val * scale,
            )

        drawn_edges = set()
        for u in graph.get_nodes():
            for v in graph.get_neighbors(u):
                edge = tuple(sorted((u, v)))
                if edge in drawn_edges:
                    continue
                drawn_edges.add(edge)
                x1, y1 = project(*positions[u])
                x2, y2 = project(*positions[v])
                canvas.create_line(x1, y1, x2, y2, fill=EDGE_COLOR, width=2)

        for node, (x_pos, y_pos) in positions.items():
            cx, cy = project(x_pos, y_pos)
            canvas.create_oval(
                cx - NODE_RADIUS,
                cy - NODE_RADIUS,
                cx + NODE_RADIUS,
                cy + NODE_RADIUS,
                fill=color_fn(node),
                outline=OUTLINE_COLOR,
                width=2,
            )
            canvas.create_text(cx, cy, text=str(node), fill="#212121", font=("Segoe UI", 11, "bold"))

    def _compute_positions(self, graph) -> NodePositions:
        nodes = sorted(graph.get_nodes())
        if not nodes:
            return {}

        angle_step = (2 * math.pi) / len(nodes)
        return {
            node: (
                math.cos(index * angle_step),
                math.sin(index * angle_step),
            )
            for index, node in enumerate(nodes)
        }

    @staticmethod
    def _color_graph1(node, current_node, visited_nodes):
        if node == current_node:
            return "#ffb74d"
        if node in visited_nodes:
            return "#66bb6a"
        return "#90caf9"

    @staticmethod
    def _color_graph2(node, candidate, visited_nodes, rejected_nodes):
        if node == candidate:
            return "#ab47bc"
        if node in rejected_nodes:
            return "#ef5350"
        if node in visited_nodes:
            return "#66bb6a"
        return "#90caf9"

    @staticmethod
    def _format_mapping(mapping: Dict[str, str]) -> str:
        if not mapping:
            return "(empty)"
        pairs = [f"{src} → {dst}" for src, dst in sorted(mapping.items())]
        return "\n".join(pairs)
