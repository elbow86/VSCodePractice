from __future__ import annotations

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

# Ensure StateMachine-Expt is importable when running from repo root.
_STATE_MACHINE_DIR = Path(__file__).resolve().parents[1]
if str(_STATE_MACHINE_DIR) not in sys.path:
    sys.path.insert(0, str(_STATE_MACHINE_DIR))

from state_pattern_example import Product, VendingMachine  # noqa: E402
from ui.tk_state_graph import GraphEdge, GraphNode, StateGraphCanvas  # noqa: E402


class VendingMachineVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine State Visualizer")

        self._machine = VendingMachine()

        main = ttk.Frame(self, padding=10)
        main.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)

        header = ttk.Frame(main)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        self._status_var = tk.StringVar(value="")
        ttk.Label(header, textvariable=self._status_var).grid(row=0, column=0, sticky="w")

        self._graph = StateGraphCanvas(main, width=620, height=300)
        self._graph.grid(row=1, column=0, sticky="nsew", pady=(10, 10))

        controls = ttk.Frame(main)
        controls.grid(row=2, column=0, sticky="ew")

        ttk.Label(controls, text="Amount:").grid(row=0, column=0, sticky="w")
        self._amount_var = tk.StringVar(value="1.00")
        ttk.Entry(controls, textvariable=self._amount_var, width=10).grid(row=0, column=1, sticky="w", padx=(6, 12))
        ttk.Button(controls, text="Insert Coin", command=self._insert_coin).grid(row=0, column=2, sticky="w")

        ttk.Label(controls, text="Product:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self._product_var = tk.StringVar(value=Product.SODA.name)
        product_names = [p.name for p in Product]
        ttk.Combobox(controls, textvariable=self._product_var, values=product_names, state="readonly", width=12).grid(
            row=1, column=1, sticky="w", padx=(6, 12), pady=(8, 0)
        )
        ttk.Button(controls, text="Select", command=self._select_product).grid(row=1, column=2, sticky="w", pady=(8, 0))

        ttk.Button(controls, text="Dispense", command=self._dispense).grid(row=0, column=3, sticky="w", padx=(14, 0))
        ttk.Button(controls, text="Return Change", command=self._return_change).grid(row=1, column=3, sticky="w", padx=(14, 0), pady=(8, 0))

        ttk.Button(controls, text="Out of Order", command=self._out_of_order).grid(row=0, column=4, sticky="w", padx=(14, 0))
        ttk.Button(controls, text="Set Operational", command=self._set_operational).grid(row=1, column=4, sticky="w", padx=(14, 0), pady=(8, 0))

        ttk.Button(controls, text="Reset", command=self._reset).grid(row=0, column=5, sticky="w", padx=(14, 0))

        self._init_graph()
        self._refresh()

    def _init_graph(self) -> None:
        nodes = [
            GraphNode("Idle", "Idle"),
            GraphNode("Coin Inserted", "Coin Inserted"),
            GraphNode("Product Selected", "Product Selected"),
            GraphNode("Out of Order", "Out of Order"),
        ]
        edges = [
            GraphEdge("Idle", "Coin Inserted", "insert"),
            GraphEdge("Coin Inserted", "Product Selected", "select"),
            GraphEdge("Coin Inserted", "Idle", "return"),
            GraphEdge("Product Selected", "Idle", "dispense"),
            GraphEdge("Product Selected", "Idle", "return"),
            GraphEdge("Idle", "Out of Order", "fault"),
            GraphEdge("Coin Inserted", "Out of Order", "fault"),
            GraphEdge("Product Selected", "Out of Order", "fault"),
            GraphEdge("Out of Order", "Idle", "repair"),
        ]
        self._graph.set_graph(nodes, edges)

    def _refresh(self) -> None:
        state = self._machine.get_current_state()
        balance = self._machine.get_balance()
        selected = self._machine.get_selected_product()
        selected_text = selected.product_name if selected else "(none)"
        self._status_var.set(f"State: {state} | Balance: ${balance:.2f} | Selected: {selected_text}")
        self._graph.set_active(state)

    def _parse_amount(self) -> float:
        try:
            amount = float(self._amount_var.get().strip())
        except ValueError:
            return 0.0
        return amount

    def _selected_product(self) -> Product:
        name = self._product_var.get().strip()
        try:
            return Product[name]
        except KeyError:
            return Product.SODA

    def _insert_coin(self) -> None:
        self._machine.insert_coin(self._parse_amount())
        self._refresh()

    def _select_product(self) -> None:
        self._machine.select_product(self._selected_product())
        self._refresh()

    def _dispense(self) -> None:
        self._machine.dispense_product()
        self._refresh()

    def _return_change(self) -> None:
        self._machine.return_change()
        self._refresh()

    def _out_of_order(self) -> None:
        self._machine.set_out_of_order()
        self._refresh()

    def _set_operational(self) -> None:
        self._machine.set_operational()
        self._refresh()

    def _reset(self) -> None:
        self._machine = VendingMachine()
        self._refresh()


def main() -> None:
    app = VendingMachineVisualizer()
    app.mainloop()


if __name__ == "__main__":
    main()
