"""Main GUI for Sliding Window Protocol Simulator."""

import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import APP_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from simulation.simulator import Simulator
from gui.animation_panel import AnimationPanel
from gui.comparison_panel import ComparisonPanel


class MainWindow:
    """Main application window."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(950, 750)
        self.root.configure(bg="#F3F6FA")

        self.simulator = Simulator()
        self.comparison_window = None
        self.comparison_panel = None

        self.setup_styles()
        self.create_header()
        self.create_main_content()
        self.create_status_bar()

    # ------------------------------------------------
    # STYLES
    # ------------------------------------------------

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TFrame",
            background="#F3F6FA"
        )

        style.configure(
            "TLabel",
            background="#F3F6FA",
            foreground="#1E293B",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Title.TLabel",
            background="#14213D",
            foreground="white",
            font=("Segoe UI", 17, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#14213D",
            foreground="#CBD5E1",
            font=("Segoe UI", 9)
        )

        style.configure(
            "Start.TButton",
            background="#16A34A",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.configure(
            "Compare.TButton",
            background="#2563EB",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

    # ------------------------------------------------
    # HEADER
    # ------------------------------------------------

    def create_header(self):
        header = tk.Frame(
            self.root,
            bg="#14213D",
            height=75
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        ttk.Label(
            header,
            text="SLIDING WINDOW PROTOCOL SIMULATOR",
            style="Title.TLabel"
        ).pack(anchor="w", padx=22, pady=(12, 2))

        ttk.Label(
            header,
            text="Interactive Computer Networks Simulation",
            style="Subtitle.TLabel"
        ).pack(anchor="w", padx=24)

    # ------------------------------------------------
    # MAIN CONTENT
    # ------------------------------------------------

    def create_main_content(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        # CONFIGURATION
        config_frame = ttk.LabelFrame(
            main,
            text="Simulation Configuration",
            padding=10
        )
        config_frame.pack(fill="x", pady=5)

        ttk.Label(
            config_frame,
            text="Select Protocol:"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.protocol_var = tk.StringVar(
            value="One-Bit Sliding Window"
        )

        ttk.Combobox(
            config_frame,
            textvariable=self.protocol_var,
            values=[
                "One-Bit Sliding Window",
                "Go-Back-N",
                "Selective Repeat"
            ],
            state="readonly",
            width=25
        ).grid(row=0, column=1, padx=8)

        ttk.Label(
            config_frame,
            text="Window Size:"
        ).grid(row=0, column=2, padx=5)

        self.window_var = tk.StringVar(value="4")

        ttk.Entry(
            config_frame,
            textvariable=self.window_var,
            width=10
        ).grid(row=0, column=3, padx=8)

        ttk.Label(
            config_frame,
            text="Number of Frames:"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.frames_var = tk.StringVar(value="10")

        ttk.Entry(
            config_frame,
            textvariable=self.frames_var,
            width=10
        ).grid(row=1, column=1, sticky="w", padx=8)

        ttk.Label(
            config_frame,
            text="Transmission Delay (ms):"
        ).grid(row=1, column=2, padx=5)

        self.transmission_var = tk.StringVar(value="100")

        ttk.Entry(
            config_frame,
            textvariable=self.transmission_var,
            width=10
        ).grid(row=1, column=3, padx=8)

        ttk.Label(
            config_frame,
            text="ACK Delay (ms):"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.ack_var = tk.StringVar(value="50")

        ttk.Entry(
            config_frame,
            textvariable=self.ack_var,
            width=10
        ).grid(row=2, column=1, padx=8)

        ttk.Label(
            config_frame,
            text="Packet Loss (%):"
        ).grid(row=2, column=2, padx=5)

        self.packet_loss_var = tk.StringVar(value="10")

        ttk.Entry(
            config_frame,
            textvariable=self.packet_loss_var,
            width=10
        ).grid(row=2, column=3, padx=8)

        ttk.Label(
            config_frame,
            text="ACK Loss (%):"
        ).grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.ack_loss_var = tk.StringVar(value="5")

        ttk.Entry(
            config_frame,
            textvariable=self.ack_loss_var,
            width=10
        ).grid(row=3, column=1, padx=8)

        ttk.Label(
            config_frame,
            text="Timeout (ms):"
        ).grid(row=3, column=2, padx=5)

        self.timeout_var = tk.StringVar(value="300")

        ttk.Entry(
            config_frame,
            textvariable=self.timeout_var,
            width=10
        ).grid(row=3, column=3, padx=8)

        # BUTTONS
        controls = ttk.Frame(main)
        controls.pack(fill="x", pady=7)

        ttk.Button(
            controls,
            text="▶ Start Simulation",
            style="Start.TButton",
            command=self.start_simulation
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="📊 Compare All Protocols",
            style="Compare.TButton",
            command=self.compare_protocols
        ).pack(side="left", padx=5)

        ttk.Button(
            controls,
            text="↻ Reset",
            command=self.reset_simulation
        ).pack(side="left", padx=5)

        # ANIMATION PANEL
        animation_frame = ttk.LabelFrame(
            main,
            text="Animated Sender-Receiver Communication",
            padding=8
        )
        animation_frame.pack(fill="x", pady=5)

        self.animation_panel = AnimationPanel(animation_frame)
        self.animation_panel.pack(fill="both", expand=True)

        # EVENT LOG
        log_frame = ttk.LabelFrame(
            main,
            text="Simulation Event Log",
            padding=8
        )
        log_frame.pack(fill="both", expand=True, pady=5)

        self.event_log = tk.Text(
            log_frame,
            height=6,
            font=("Consolas", 9),
            wrap="word",
            bg="white",
            fg="#1E293B",
            state="disabled"
        )
        self.event_log.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            log_frame,
            orient="vertical",
            command=self.event_log.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.event_log.configure(
            yscrollcommand=scrollbar.set
        )

        # PERFORMANCE RESULTS
        results_frame = ttk.LabelFrame(
            main,
            text="Performance Results",
            padding=8
        )
        results_frame.pack(fill="x", pady=5)

        self.results_label = ttk.Label(
            results_frame,
            text="Run a simulation to view results.",
            justify="left"
        )
        self.results_label.pack(anchor="w")

    # ------------------------------------------------
    # STATUS BAR
    # ------------------------------------------------

    def create_status_bar(self):
        self.status_label = tk.Label(
            self.root,
            text="Status: Ready",
            bg="#14213D",
            fg="white",
            anchor="w",
            padx=12,
            pady=6
        )
        self.status_label.pack(fill="x")

    # ------------------------------------------------
    # READ AND VALIDATE INPUTS
    # ------------------------------------------------

    def get_simulation_inputs(self):
        protocol = self.protocol_var.get()

        frames = int(self.frames_var.get())
        window = int(self.window_var.get())

        transmission = float(self.transmission_var.get())
        ack = float(self.ack_var.get())

        packet_loss = float(self.packet_loss_var.get())
        ack_loss = float(self.ack_loss_var.get())

        timeout = float(self.timeout_var.get())

        if frames < 1:
            raise ValueError("Number of frames must be at least 1.")

        if window < 1:
            raise ValueError("Window size must be at least 1.")

        if transmission <= 0 or ack <= 0:
            raise ValueError("Transmission and ACK delays must be positive.")

        if timeout <= 0:
            raise ValueError("Timeout must be positive.")

        if not 0 <= packet_loss <= 100:
            raise ValueError("Packet loss must be between 0 and 100.")

        if not 0 <= ack_loss <= 100:
            raise ValueError("ACK loss must be between 0 and 100.")

        return {
            "protocol": protocol,
            "frames": frames,
            "window": window,
            "transmission": transmission,
            "ack": ack,
            "packet_loss": packet_loss,
            "ack_loss": ack_loss,
            "timeout": timeout
        }

    # ------------------------------------------------
    # DISPLAY EVENT LOG
    # ------------------------------------------------

    def display_events(self, events):
        self.event_log.config(state="normal")
        self.event_log.delete("1.0", tk.END)

        for event in events:
            self.event_log.insert(tk.END, event + "\n")

        self.event_log.config(state="disabled")
        self.event_log.see(tk.END)

    # ------------------------------------------------
    # START SINGLE PROTOCOL SIMULATION
    # ------------------------------------------------

    def start_simulation(self):
        try:
            inputs = self.get_simulation_inputs()

            protocol = inputs["protocol"]

            self.animation_panel.reset()

            self.status_label.config(
                text=f"Status: Running {protocol}..."
            )

            self.root.update_idletasks()

            results = self.simulator.run_simulation(
                protocol_name=protocol,
                number_of_frames=inputs["frames"],
                window_size=inputs["window"],
                transmission_delay=inputs["transmission"],
                ack_delay=inputs["ack"],
                packet_loss=inputs["packet_loss"],
                ack_loss=inputs["ack_loss"],
                timeout=inputs["timeout"]
            )

            # Display event log
            self.display_events(results["events"])

            # Start animation
            self.animation_panel.play(results["events"])

            # Display performance
            output = (
                f"Protocol: {protocol}\n"
                f"Total Frames Transmitted: "
                f"{results['total_frames_transmitted']}\n"
                f"Retransmissions: {results['retransmissions']}\n"
                f"Packets Lost: {results['packets_lost']}\n"
                f"ACKs Received: {results['acks_received']}\n"
                f"Total Transmission Time: "
                f"{results['total_time_ms']} ms\n"
                f"Throughput: {results['throughput_fps']} frames/sec\n"
                f"Efficiency: {results['efficiency_percent']}%"
            )

            self.results_label.config(text=output)

            self.status_label.config(
                text=f"Status: {protocol} simulation completed"
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid Input", str(error))

        except Exception as error:
            messagebox.showerror("Simulation Error", str(error))

    # ------------------------------------------------
    # COMPARE ALL THREE PROTOCOLS
    # ------------------------------------------------

    def compare_protocols(self):
        try:
            inputs = self.get_simulation_inputs()

            protocol_names = [
                "One-Bit Sliding Window",
                "Go-Back-N",
                "Selective Repeat"
            ]

            comparison_results = {}

            self.status_label.config(
                text="Status: Comparing all three protocols..."
            )

            self.root.update_idletasks()

            for protocol in protocol_names:
                results = self.simulator.run_simulation(
                    protocol_name=protocol,
                    number_of_frames=inputs["frames"],
                    window_size=inputs["window"],
                    transmission_delay=inputs["transmission"],
                    ack_delay=inputs["ack"],
                    packet_loss=inputs["packet_loss"],
                    ack_loss=inputs["ack_loss"],
                    timeout=inputs["timeout"]
                )

                comparison_results[protocol] = results

            # Create comparison window if it does not exist
            if (
                self.comparison_window is None
                or not self.comparison_window.winfo_exists()
            ):
                self.comparison_window = tk.Toplevel(self.root)
                self.comparison_window.title(
                    "Protocol Performance Comparison"
                )
                self.comparison_window.geometry("950x550")
                self.comparison_window.minsize(750, 450)

                self.comparison_panel = ComparisonPanel(
                    self.comparison_window
                )
                self.comparison_panel.pack(
                    fill="both",
                    expand=True,
                    padx=10,
                    pady=10
                )

            # Update graph with latest results
            self.comparison_panel.update_graph(comparison_results)

            self.comparison_window.lift()

            self.status_label.config(
                text="Status: Protocol comparison completed"
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid Input", str(error))

        except Exception as error:
            messagebox.showerror("Comparison Error", str(error))

    # ------------------------------------------------
    # RESET
    # ------------------------------------------------

    def reset_simulation(self):
        self.animation_panel.reset()

        self.event_log.config(state="normal")
        self.event_log.delete("1.0", tk.END)
        self.event_log.config(state="disabled")

        self.results_label.config(
            text="Run a simulation to view results."
        )

        if (
            self.comparison_window is not None
            and self.comparison_window.winfo_exists()
        ):
            self.comparison_panel.reset()

        self.status_label.config(text="Status: Ready")

    # ------------------------------------------------
    # RUN
    # ------------------------------------------------

    def run(self):
        self.root.mainloop()