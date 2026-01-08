from __future__ import annotations

from dataclasses import dataclass
from tkinter import Canvas
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class GraphNode:
    key: str
    label: str


@dataclass(frozen=True)
class GraphEdge:
    src: str
    dst: str
    label: str = ""


class StateGraphCanvas(Canvas):
    """A lightweight directed state graph widget.

    - Draws nodes (circles) and directed edges.
    - Highlights the active node.

    Colors are kept to basic Tk defaults to avoid introducing new theme tokens.
    """

    def __init__(
        self,
        master,
        *,
        width: int = 520,
        height: int = 260,
        node_radius: int = 28,
        **kwargs,
    ):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)
        self._node_radius = node_radius

        self._nodes: List[GraphNode] = []
        self._edges: List[GraphEdge] = []
        self._positions: Dict[str, Tuple[int, int]] = {}
        self._active_key: Optional[str] = None

    def set_graph(self, nodes: Iterable[GraphNode], edges: Iterable[GraphEdge]) -> None:
        self._nodes = list(nodes)
        self._edges = list(edges)
        self._layout_nodes()
        self.redraw()

    def set_active(self, key: Optional[str]) -> None:
        self._active_key = key
        self.redraw()

    def _layout_nodes(self) -> None:
        # Simple circular layout.
        width = int(self["width"])
        height = int(self["height"])

        if not self._nodes:
            self._positions = {}
            return

        cx, cy = width // 2, height // 2
        radius = max(60, min(width, height) // 2 - 50)

        import math

        n = len(self._nodes)
        self._positions = {}
        for i, node in enumerate(self._nodes):
            angle = (2 * math.pi * i) / n
            x = int(cx + radius * math.cos(angle))
            y = int(cy + radius * math.sin(angle))
            self._positions[node.key] = (x, y)

    def redraw(self) -> None:
        self.delete("all")

        # Draw edges first.
        for edge in self._edges:
            src = self._positions.get(edge.src)
            dst = self._positions.get(edge.dst)
            if not src or not dst:
                continue
            self._draw_arrow(src, dst)
            if edge.label:
                mx = (src[0] + dst[0]) // 2
                my = (src[1] + dst[1]) // 2
                self.create_text(mx, my - 10, text=edge.label, anchor="center")

        # Draw nodes.
        for node in self._nodes:
            pos = self._positions.get(node.key)
            if not pos:
                continue
            self._draw_node(node, pos, active=(node.key == self._active_key))

    def _draw_node(self, node: GraphNode, pos: Tuple[int, int], *, active: bool) -> None:
        x, y = pos
        r = self._node_radius

        fill = "white"
        outline = "black"
        width = 3 if active else 2

        self.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline=outline, width=width)
        self.create_text(x, y, text=node.label, anchor="center")

    def _draw_arrow(self, src: Tuple[int, int], dst: Tuple[int, int]) -> None:
        # Draw a straight arrow; trim so it doesn't overlap node circles.
        import math

        sx, sy = src
        dx, dy = dst
        vx, vy = dx - sx, dy - sy
        dist = math.hypot(vx, vy)
        if dist == 0:
            return

        r = self._node_radius
        ux, uy = vx / dist, vy / dist

        start_x = sx + int(ux * r)
        start_y = sy + int(uy * r)
        end_x = dx - int(ux * r)
        end_y = dy - int(uy * r)

        self.create_line(start_x, start_y, end_x, end_y, arrow="last", width=2)
