"""Separate window for comparing protocol performance results."""

import tkinter as tk
from tkinter import ttk


class ResultsPanel(tk.Toplevel):
    """Display actual results from the latest all-protocol comparison."""

    METRICS = (
        ("Total Frames Transmitted", "total_frames_transmitted"),
        ("Retransmissions", "retransmissions"),
        ("Packets Lost", "packets_lost"),
        ("ACKs Received", "acks_received"),
        ("Delivered Frames", "delivered_frames"),
        ("Total Transmission Time (ms)", "total_time_ms"),
        ("Throughput (frames/sec)", "throughput_fps"),
        ("Efficiency (%)", "efficiency_percent"),
    )

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Protocol Performance Results")
        self.geometry("1040x600")
        self.minsize(900, 520)
        self.configure(background="#F3F6FA")
        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        header = tk.Frame(self, background="#14213D", padx=20, pady=14)
        header.pack(fill="x")
        tk.Label(
            header,
            text="PROTOCOL PERFORMANCE COMPARISON",
            background="#14213D",
            foreground="white",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Numerical results from the latest simulation of all three protocols",
            background="#14213D",
            foreground="#CBD5E1",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        content = ttk.Frame(self, padding=(18, 12))
        content.pack(fill="both", expand=True)

        self.parameters_label = ttk.Label(
            content,
            text="",
            justify="left",
            font=("Segoe UI", 10),
            wraplength=980,
        )
        self.parameters_label.pack(anchor="w", pady=(0, 10))

        self.message_label = ttk.Label(
            content,
            text="Please run Compare All Protocols first.",
            font=("Segoe UI", 11),
        )
        self.message_label.pack(anchor="w", pady=(0, 8))

        table_frame = ttk.Frame(content)
        table_frame.pack(fill="both", expand=True)

        columns = ("metric", "stop_and_wait", "Go-Back-N", "Selective Repeat")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8,
        )

        headings = {
            "metric": "Performance Metric",
            "stop_and_wait": "Stop-and-Wait",
            "Go-Back-N": "Go-Back-N",
            "Selective Repeat": "Selective Repeat",
        }
        widths = {
            "metric": 310,
            "stop_and_wait": 190,
            "Go-Back-N": 190,
            "Selective Repeat": 210,
        }
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(
                column,
                width=widths[column],
                minwidth=140 if column != "metric" else 240,
                anchor="w" if column == "metric" else "center",
                stretch=True,
            )

        self.tree.tag_configure("odd", background="#FFFFFF")
        self.tree.tag_configure("even", background="#EAF0F7")
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(
            content,
            text="Close",
            command=self.withdraw,
        ).pack(anchor="e", pady=(12, 0))

        self.clear()

    @staticmethod
    def _format_value(value):
        if value is None or value == "":
            return "—"
        if isinstance(value, float):
            return f"{value:.2f}"
        return str(value)

    def update_results(self, results, parameters):
        """Refresh the table and parameter summary from stored simulation data."""
        self.tree.delete(*self.tree.get_children())
        self.message_label.pack_forget()

        self.parameters_label.configure(
            text=(
                f"Frames: {parameters['frames']}    "
                f"Window size: {parameters['window']}    "
                f"Transmission delay: {parameters['transmission']} ms    "
                f"ACK delay: {parameters['ack']} ms\n"
                f"Packet loss: {parameters['packet_loss']}%    "
                f"ACK loss: {parameters['ack_loss']}%    "
                f"Timeout: {parameters['timeout']} ms"
            )
        )

        protocol_keys = (
            "One-Bit Sliding Window",
            "Go-Back-N",
            "Selective Repeat",
        )
        for index, (label, metric_key) in enumerate(self.METRICS):
            row = [label]
            for protocol in protocol_keys:
                protocol_result = results.get(protocol, {})
                row.append(
                    self._format_value(protocol_result.get(metric_key))
                )
            self.tree.insert(
                "",
                "end",
                values=row,
                tags=("even" if index % 2 else "odd",),
            )

    def clear(self):
        """Remove any previously displayed comparison and show the prompt."""
        self.tree.delete(*self.tree.get_children())
        self.parameters_label.configure(text="")
        self.message_label.configure(
            text="Please run Compare All Protocols first."
        )
        self.message_label.pack(anchor="w", pady=(0, 8))
