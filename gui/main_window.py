"""Main GUI for Sliding Window Protocol Simulator."""

import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import APP_TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from simulation.simulator import Simulator
from gui.animation_panel import AnimationPanel
from gui.comparison_panel import ComparisonPanel
from gui.results_panel import ResultsPanel


class MainWindow:
    """Main application window."""

    PROTOCOL_ORDER = [
        "One-Bit Sliding Window",
        "Go-Back-N",
        "Selective Repeat",
    ]

    SCENARIOS = {
        "Ideal Network": {
            "frames": 20,
            "window": 4,
            "transmission": 10,
            "ack": 5,
            "packet_loss": 0,
            "ack_loss": 0,
            "timeout": 50,
            "seed": 101,
        },
        "Packet Loss": {
            "frames": 20,
            "window": 4,
            "transmission": 10,
            "ack": 5,
            "packet_loss": 20,
            "ack_loss": 0,
            "timeout": 50,
            "seed": 202,
        },
        "ACK Loss": {
            "frames": 20,
            "window": 4,
            "transmission": 10,
            "ack": 5,
            "packet_loss": 0,
            "ack_loss": 20,
            "timeout": 50,
            "seed": 303,
        },
        "Combined Loss": {
            "frames": 20,
            "window": 4,
            "transmission": 10,
            "ack": 5,
            "packet_loss": 20,
            "ack_loss": 10,
            "timeout": 50,
            "seed": 404,
        },
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(950, 750)
        self.root.configure(bg="#F3F6FA")

        self.simulator = Simulator()
        self.comparison_window = None
        self.comparison_panel = None
        self.results_panel = None
        self.current_comparison_results = {}
        self.current_comparison_parameters = {}
        self.current_scenario_name = "Ideal Network"

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
            text="Scenario:"
        ).grid(row=0, column=2, sticky="w", padx=5, pady=5)

        self.scenario_var = tk.StringVar(value="Ideal Network")
        scenario_combo = ttk.Combobox(
            config_frame,
            textvariable=self.scenario_var,
            values=list(self.SCENARIOS.keys()),
            state="readonly",
            width=18
        )
        scenario_combo.grid(row=0, column=3, padx=8)
        self.scenario_var.trace_add("write", self._on_scenario_change)

        ttk.Label(
            config_frame,
            text="Window Size:"
        ).grid(row=1, column=0, padx=5)

        self.window_var = tk.StringVar(value="4")

        ttk.Entry(
            config_frame,
            textvariable=self.window_var,
            width=10
        ).grid(row=1, column=1, padx=8)

        ttk.Label(
            config_frame,
            text="Number of Frames:"
        ).grid(row=1, column=2, padx=5)

        self.frames_var = tk.StringVar(value="20")

        ttk.Entry(
            config_frame,
            textvariable=self.frames_var,
            width=10
        ).grid(row=1, column=3, padx=8)

        ttk.Label(
            config_frame,
            text="Transmission Delay (ms):"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.transmission_var = tk.StringVar(value="10")

        ttk.Entry(
            config_frame,
            textvariable=self.transmission_var,
            width=10
        ).grid(row=2, column=1, padx=8)

        ttk.Label(
            config_frame,
            text="ACK Delay (ms):"
        ).grid(row=2, column=2, padx=5)

        self.ack_var = tk.StringVar(value="5")

        ttk.Entry(
            config_frame,
            textvariable=self.ack_var,
            width=10
        ).grid(row=2, column=3, padx=8)

        ttk.Label(
            config_frame,
            text="Packet Loss (%):"
        ).grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.packet_loss_var = tk.StringVar(value="0")

        ttk.Entry(
            config_frame,
            textvariable=self.packet_loss_var,
            width=10
        ).grid(row=3, column=1, padx=8)

        ttk.Label(
            config_frame,
            text="ACK Loss (%):"
        ).grid(row=3, column=2, padx=5)

        self.ack_loss_var = tk.StringVar(value="0")

        ttk.Entry(
            config_frame,
            textvariable=self.ack_loss_var,
            width=10
        ).grid(row=3, column=3, padx=8)

        ttk.Label(
            config_frame,
            text="Timeout (ms):"
        ).grid(row=4, column=0, sticky="w", padx=5, pady=5)

        self.timeout_var = tk.StringVar(value="50")

        ttk.Entry(
            config_frame,
            textvariable=self.timeout_var,
            width=10
        ).grid(row=4, column=1, padx=8)

        self.apply_scenario("Ideal Network")

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
            text="View Performance Results",
            command=self.view_performance_results
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
        animation_frame.pack(fill="both", expand=True, pady=5)

        self.animation_panel = AnimationPanel(animation_frame)
        self.animation_panel.pack(fill="both", expand=True)

        # EVENT LOG
        log_frame = ttk.LabelFrame(
            main,
            text="Simulation Event Log",
            padding=8
        )
        log_frame.pack(fill="both", expand=True, pady=5)

        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill="x", pady=(0, 2))

        self.pause_button = ttk.Button(
            log_controls,
            text="Pause",
            command=self._pause_simulation,
            state="disabled"
        )
        self.pause_button.pack(side="left", padx=(0, 4))

        self.resume_button = ttk.Button(
            log_controls,
            text="Resume",
            command=self._resume_simulation,
            state="disabled"
        )
        self.resume_button.pack(side="left", padx=4)

        self.step_button = ttk.Button(
            log_controls,
            text="Step Forward",
            command=self._step_simulation,
            state="disabled"
        )
        self.step_button.pack(side="left", padx=4)

        ttk.Button(
            log_controls,
            text="Clear Log",
            command=self._clear_event_log
        ).pack(side="left", padx=4)

        self.event_count_var = tk.StringVar(value="Events: 0")
        self.event_status_var = tk.StringVar(value="Status: Ready")
        ttk.Label(
            log_controls,
            textvariable=self.event_count_var
        ).pack(side="right", padx=6)
        ttk.Label(
            log_controls,
            textvariable=self.event_status_var
        ).pack(side="right", padx=6)

        event_table = ttk.Frame(log_frame)
        event_table.pack(fill="both", expand=True)
        columns = (
            "step", "time", "protocol", "event", "frame_ack", "status"
        )
        self.event_log = ttk.Treeview(
            event_table,
            columns=columns,
            show="headings",
            height=2,
        )
        headings = {
            "step": ("Step", 52),
            "time": ("Time (ms)", 76),
            "protocol": ("Protocol", 118),
            "event": ("Event", 360),
            "frame_ack": ("Frame / ACK", 92),
            "status": ("Status", 105),
        }
        for column, (heading, width) in headings.items():
            self.event_log.heading(column, text=heading)
            self.event_log.column(
                column,
                width=width,
                minwidth=45,
                anchor="w" if column in ("event", "protocol") else "center",
                stretch=column == "event",
            )

        event_scrollbar = ttk.Scrollbar(
            event_table,
            orient="vertical",
            command=self.event_log.yview
        )
        self.event_log.configure(yscrollcommand=event_scrollbar.set)
        self.event_log.pack(side="left", fill="both", expand=True)
        event_scrollbar.pack(side="right", fill="y")
        self.event_log.tag_configure(
            "data_success", background="#EFF6FF", foreground="#1D4ED8"
        )
        self.event_log.tag_configure(
            "ack_success", background="#F0FDF4", foreground="#15803D"
        )
        self.event_log.tag_configure(
            "packet_loss", background="#FEF2F2", foreground="#B91C1C"
        )
        self.event_log.tag_configure(
            "ack_loss", background="#FEF2F2", foreground="#B91C1C"
        )
        self.event_log.tag_configure(
            "retransmission", background="#FFF7ED", foreground="#C2410C"
        )
        self.event_log.tag_configure(
            "timeout", background="#FFF7ED", foreground="#C2410C"
        )
        self.event_log.tag_configure(
            "discarded", background="#F1F5F9", foreground="#475569"
        )
        self.event_log.tag_configure(
            "received", background="#F0FDF4", foreground="#166534"
        )
        self.event_log.tag_configure(
            "current", font=("Segoe UI", 9, "bold")
        )
        self.current_log_item = None

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
    # SCENARIO HANDLING
    # ------------------------------------------------

    def _on_scenario_change(self, *args):
        scenario_name = self.scenario_var.get()
        if scenario_name in self.SCENARIOS:
            self.apply_scenario(scenario_name)

    def apply_scenario(self, scenario_name):
        if scenario_name not in self.SCENARIOS:
            return

        self.current_scenario_name = scenario_name
        params = self.SCENARIOS[scenario_name]

        self.frames_var.set(str(params["frames"]))
        self.window_var.set(str(params["window"]))
        self.transmission_var.set(str(params["transmission"]))
        self.ack_var.set(str(params["ack"]))
        self.packet_loss_var.set(str(params["packet_loss"]))
        self.ack_loss_var.set(str(params["ack_loss"]))
        self.timeout_var.set(str(params["timeout"]))

    def get_seed_for_current_scenario(self):
        scenario_name = self.scenario_var.get()
        return self.SCENARIOS.get(scenario_name, {}).get("seed", 1)

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
        self._clear_event_log()
        for event in events:
            self.event_log.insert(
                "", "end",
                values=("", "", "", event.strip(), "", "")
            )
        self.event_count_var.set(f"Events: {len(self.event_log.get_children())}")
        children = self.event_log.get_children()
        if children:
            self.event_log.see(children[-1])

    def _clear_event_log(self):
        self.event_log.delete(*self.event_log.get_children())
        self.current_log_item = None
        self.event_count_var.set("Events: 0")

    def _append_simulation_event(self, record):
        if self.current_log_item:
            tags = tuple(
                tag for tag in self.event_log.item(
                    self.current_log_item, "tags"
                ) if tag != "current"
            )
            self.event_log.item(self.current_log_item, tags=tags)

        kind = record["kind"]
        if kind == "data_tx":
            if not record["transmission_succeeded"]:
                row_tag = "packet_loss"
            else:
                row_tag = (
                    "retransmission" if record["attempt"] > 1
                    else "data_success"
                )
        elif kind == "data_lost":
            row_tag = "packet_loss"
        elif kind in ("ack_generated", "ack_received"):
            row_tag = (
                "ack_success" if record["transmission_succeeded"] is not False
                else "ack_loss"
            )
        elif kind == "ack_lost":
            row_tag = "ack_loss"
        elif kind == "timeout":
            row_tag = "timeout"
        elif kind == "retransmit":
            row_tag = "retransmission"
        elif kind in ("duplicate", "discard"):
            row_tag = "discarded"
        elif kind in ("received", "delivered", "buffered"):
            row_tag = "received"
        else:
            row_tag = ""

        tags = (row_tag, "current") if row_tag else ("current",)
        self.current_log_item = self.event_log.insert(
            "", "end",
            values=(
                record["step"],
                f"{record['time_ms']:.1f}",
                record["protocol"],
                record["event"],
                record["frame_ack"],
                record["status"],
            ),
            tags=tags,
        )
        self.event_count_var.set(
            f"Events: {len(self.event_log.get_children())}"
        )
        self.event_log.see(self.current_log_item)
        self.event_status_var.set(
            f"Status: Running — {record['status']}"
        )

    def _pause_simulation(self):
        self.animation_panel.pause()
        self.event_status_var.set("Status: Paused")
        self.pause_button.configure(state="disabled")
        self.resume_button.configure(state="normal")

    def _resume_simulation(self):
        self.animation_panel.resume()
        self.event_status_var.set("Status: Running")
        self.pause_button.configure(state="normal")
        self.resume_button.configure(state="disabled")

    def _step_simulation(self):
        self.animation_panel.step_forward()
        self.event_status_var.set("Status: Stepping")
        self.pause_button.configure(state="disabled")
        self.resume_button.configure(state="normal")

    def _simulation_state_changed(self, state):
        self.event_status_var.set(f"Status: {state}")
        if state == "Paused":
            self.pause_button.configure(state="disabled")
            self.resume_button.configure(state="normal")
        elif state == "Running":
            self.pause_button.configure(state="normal")
            self.resume_button.configure(state="disabled")

    # ------------------------------------------------
    # START SINGLE PROTOCOL SIMULATION
    # ------------------------------------------------

    def start_simulation(self):
        try:
            inputs = self.get_simulation_inputs()
            protocol = inputs["protocol"]

            self.animation_panel.reset()
            self._clear_event_log()
            self.event_status_var.set("Status: Preparing simulation")

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
                timeout=inputs["timeout"],
                seed=self.get_seed_for_current_scenario()
            )

            self.pause_button.configure(state="normal")
            self.resume_button.configure(state="disabled")
            self.step_button.configure(state="normal")
            self.event_status_var.set("Status: Running")
            self.animation_panel.play(
                results["events"],
                protocol,
                inputs,
                on_event=self._append_simulation_event,
                on_complete=lambda: self._simulation_completed(protocol),
                on_state=self._simulation_state_changed,
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid Input", str(error))

        except Exception as error:
            self.event_status_var.set("Status: Failed")
            self.pause_button.configure(state="disabled")
            self.resume_button.configure(state="disabled")
            self.step_button.configure(state="disabled")
            messagebox.showerror("Simulation Error", str(error))

    def _simulation_completed(self, protocol):
        self.event_status_var.set("Status: Completed")
        self.status_label.config(
            text=f"Status: {protocol} simulation completed"
        )
        self.pause_button.configure(state="disabled")
        self.resume_button.configure(state="disabled")
        self.step_button.configure(state="disabled")

    # ------------------------------------------------
    # COMPARE ALL THREE PROTOCOLS
    # ------------------------------------------------

    def compare_protocols(self):
        try:
            inputs = self.get_simulation_inputs()
            protocol_names = self.PROTOCOL_ORDER
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
                    timeout=inputs["timeout"],
                    seed=self.get_seed_for_current_scenario()
                )
                comparison_results[protocol] = results

            self.current_comparison_results = comparison_results
            self.current_comparison_parameters = {
                key: inputs[key]
                for key in (
                    "frames",
                    "window",
                    "transmission",
                    "ack",
                    "packet_loss",
                    "ack_loss",
                    "timeout",
                )
            }

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

            self.comparison_panel.update_graph(comparison_results)
            self.comparison_window.lift()

            if (
                self.results_panel is not None
                and self.results_panel.winfo_exists()
            ):
                self.results_panel.update_results(
                    self.current_comparison_results,
                    self.current_comparison_parameters,
                )

            self.status_label.config(
                text="Status: Protocol comparison completed"
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid Input", str(error))

        except Exception as error:
            messagebox.showerror("Comparison Error", str(error))

    def view_performance_results(self):
        if (
            self.results_panel is None
            or not self.results_panel.winfo_exists()
        ):
            self.results_panel = ResultsPanel(self.root)

        if self.current_comparison_results:
            self.results_panel.update_results(
                self.current_comparison_results,
                self.current_comparison_parameters,
            )
        else:
            self.results_panel.clear()

        self.results_panel.deiconify()
        self.results_panel.lift()

    # ------------------------------------------------
    # RESET
    # ------------------------------------------------

    def reset_simulation(self):
        self.animation_panel.reset()

        self._clear_event_log()
        self.event_status_var.set("Status: Ready")
        self.pause_button.configure(state="disabled")
        self.resume_button.configure(state="disabled")
        self.step_button.configure(state="disabled")

        self.current_comparison_results = {}
        self.current_comparison_parameters = {}

        if (
            self.results_panel is not None
            and self.results_panel.winfo_exists()
        ):
            self.results_panel.clear()
            self.results_panel.withdraw()

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