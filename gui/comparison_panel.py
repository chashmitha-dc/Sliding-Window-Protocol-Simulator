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

        self.figure = Figure(figsize=(9, 6), dpi=100)
        self.throughput_ax = self.figure.add_subplot(211)
        self.efficiency_ax = self.figure.add_subplot(212)

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
        self.throughput_ax.clear()
        self.efficiency_ax.clear()

        self.throughput_ax.set_title("Throughput Comparison")
        self.throughput_ax.set_ylabel("Frames/sec")
        self.throughput_ax.set_xlabel("Protocols")
        self.throughput_ax.grid(True, linestyle="--", alpha=0.4)

        self.efficiency_ax.set_title("Efficiency Comparison")
        self.efficiency_ax.set_ylabel("Efficiency (%)")
        self.efficiency_ax.set_xlabel("Protocols")
        self.efficiency_ax.grid(True, linestyle="--", alpha=0.4)

        self.figure.tight_layout()
        self.canvas.draw()

    def update_graph(self, results):
        """Display two separate subplots for throughput and efficiency."""

        self.results = results
        protocols = list(results.keys())

        if not protocols:
            self.show_empty_graph()
            return

        throughputs = [
            float(results[name].get("throughput_fps", 0.0))
            for name in protocols
        ]

        efficiencies = [
            float(results[name].get("efficiency_percent", 0.0))
            for name in protocols
        ]

        x = list(range(len(protocols)))
        width = 0.6

        self.throughput_ax.clear()
        bars = self.throughput_ax.bar(
            x,
            throughputs,
            width=width,
            color=["#4F46E5", "#10B981", "#F59E0B"]
        )
        self.throughput_ax.set_title("Throughput Comparison")
        self.throughput_ax.set_ylabel("Frames/sec")
        self.throughput_ax.set_xlabel("Protocols")
        self.throughput_ax.set_xticks(x)
        self.throughput_ax.set_xticklabels(protocols, rotation=0)
        self.throughput_ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        for bar, value in zip(bars, throughputs):
            height = bar.get_height()
            self.throughput_ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + max(throughputs) * 0.02,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=8
            )

        self.efficiency_ax.clear()
        bars = self.efficiency_ax.bar(
            x,
            efficiencies,
            width=width,
            color=["#4F46E5", "#10B981", "#F59E0B"]
        )
        self.efficiency_ax.set_title("Efficiency Comparison")
        self.efficiency_ax.set_ylabel("Efficiency (%)")
        self.efficiency_ax.set_xlabel("Protocols")
        self.efficiency_ax.set_xticks(x)
        self.efficiency_ax.set_xticklabels(protocols, rotation=0)
        self.efficiency_ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        for bar, value in zip(bars, efficiencies):
            height = bar.get_height()
            self.efficiency_ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 2,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=8
            )

        self.figure.tight_layout()
        self.canvas.draw()

    def reset(self):
        self.results = {}
        self.show_empty_graph()