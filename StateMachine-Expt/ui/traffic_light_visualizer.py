from __future__ import annotations

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

# Ensure StateMachine-Expt is importable when running from repo root.
_STATE_MACHINE_DIR = Path(__file__).resolve().parents[1]
if str(_STATE_MACHINE_DIR) not in sys.path:
    sys.path.insert(0, str(_STATE_MACHINE_DIR))

from simple_traffic_light import SimpleTrafficLight  # noqa: E402
from ui.tk_state_graph import GraphEdge, GraphNode, StateGraphCanvas  # noqa: E402


class TrafficLightVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traffic Light State Visualizer")

        self._light = SimpleTrafficLight()

        main = ttk.Frame(self, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        header = ttk.Frame(main)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        ttk.Label(header, text="SimpleTrafficLight").grid(row=0, column=0, sticky="w")
        self._status_var = tk.StringVar(value="")
        ttk.Label(header, textvariable=self._status_var).grid(row=0, column=1, sticky="w", padx=(12, 0))

        self._graph = StateGraphCanvas(main, width=520, height=260)
        self._graph.grid(row=1, column=0, sticky="nsew", pady=(10, 10))

        controls = ttk.Frame(main)
        controls.grid(row=2, column=0, sticky="ew")
        controls.columnconfigure(0, weight=1)

        ttk.Button(controls, text="Step (Next)", command=self._step).grid(row=0, column=0, sticky="w")
        ttk.Button(controls, text="Reset", command=self._reset).grid(row=0, column=1, sticky="w", padx=(10, 0))

        self._init_graph()
        self._refresh()

    def _init_graph(self) -> None:
        nodes = [
            GraphNode("RED", "RED"),
            GraphNode("GREEN", "GREEN"),
            GraphNode("YELLOW", "YELLOW"),
        ]
        edges = [
            GraphEdge("RED", "GREEN", "next"),
            GraphEdge("GREEN", "YELLOW", "next"),
            GraphEdge("YELLOW", "RED", "next"),
        ]
        self._graph.set_graph(nodes, edges)

    def _current_key(self) -> str:
        status = self._light.get_status()
        return status.get("color", "")

    def _refresh(self) -> None:
        status = self._light.get_status()
        crossing = "YES" if status.get("pedestrians_can_cross") else "NO"
        self._status_var.set(f"Color: {status.get('color')} | Action: {status.get('action')} | Pedestrians cross: {crossing}")
        self._graph.set_active(self._current_key())

    def _step(self) -> None:
        self._light.next_light()
        self._refresh()

    def _reset(self) -> None:
        self._light = SimpleTrafficLight()
        self._refresh()


def main() -> None:
    app = TrafficLightVisualizer()
    app.mainloop()


if __name__ == "__main__":
    main()
