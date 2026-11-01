"""Comparison graphs for sliding window protocols."""

import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ComparisonPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.results = {}

        ttk.Label(
            self,
            text="Protocol Performance Comparison",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.figure = Figure(figsize=(9, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        self.show_empty_graph()

    def show_empty_graph(self):
        self.ax.clear()
        self.ax.set_title("Run simulations to compare protocols")
        self.ax.set_ylabel("Performance")
        self.ax.set_xlabel("Protocols")
        self.canvas.draw()

    def update_graph(self, results):
        """
        results format:
        {
            "Stop-and-Wait": {"throughput_fps": 5, ...},
            "Go-Back-N": {"throughput_fps": 10, ...},
            "Selective Repeat": {"throughput_fps": 12, ...}
        }
        """

        self.results = results

        protocols = list(results.keys())

        if not protocols:
            self.show_empty_graph()
            return

        throughputs = [
            results[name]["throughput_fps"]
            for name in protocols
        ]

        efficiencies = [
            results[name]["efficiency_percent"]
            for name in protocols
        ]

        self.ax.clear()

        x = list(range(len(protocols)))
        width = 0.35

        self.ax.bar(
            [i - width / 2 for i in x],
            throughputs,
            width,
            label="Throughput (frames/sec)"
        )

        self.ax.bar(
            [i + width / 2 for i in x],
            efficiencies,
            width,
            label="Efficiency (%)"
        )

        self.ax.set_title("Protocol Performance Comparison")
        self.ax.set_xlabel("Protocols")
        self.ax.set_ylabel("Performance Value")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(protocols)
        self.ax.legend()
        self.ax.grid(axis="y", linestyle="--", alpha=0.4)

        self.figure.tight_layout()
        self.canvas.draw()

    def reset(self):
        self.results = {}
        self.show_empty_graph()