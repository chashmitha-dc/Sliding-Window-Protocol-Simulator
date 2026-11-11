"""Interactive sender-receiver timeline for ARQ simulations."""

import re
import tkinter as tk
from tkinter import ttk


_FRAME_PATTERN = re.compile(r"\bFrame\s+(\d+)\b", re.IGNORECASE)
_ACK_PATTERN = re.compile(r"\bACK\s+(\d+)\b", re.IGNORECASE)
_ATTEMPT_PATTERN = re.compile(r"\bAttempt\s+(\d+)\b", re.IGNORECASE)
_WINDOW_PATTERN = re.compile(r"\[(\d+),\s*(\d+)\]")
_SLIDE_PATTERN = re.compile(r"from\s+(\d+)\s+to\s+(\d+)", re.IGNORECASE)


def normalize_events(events, protocol, parameters):
    """Convert protocol event strings to UI records without inventing events."""

    records = []
    elapsed_ms = 0.0
    transmission_delay = float(parameters["transmission"])
    ack_delay = float(parameters["ack"])
    timeout = float(parameters["timeout"])

    for raw_event in events:
        event = raw_event.strip()
        if not event:
            continue

        lower_event = event.lower()
        frame_match = _FRAME_PATTERN.search(event)
        ack_match = _ACK_PATTERN.search(event)
        attempt_match = _ATTEMPT_PATTERN.search(event)
        window_match = _WINDOW_PATTERN.search(event)
        slide_match = _SLIDE_PATTERN.search(event)

        frame = int(frame_match.group(1)) if frame_match else None
        ack = int(ack_match.group(1)) if ack_match else None
        attempt = int(attempt_match.group(1)) if attempt_match else 1

        if "simulation started" in lower_event:
            kind = "start"
        elif "simulation completed" in lower_event:
            kind = "complete"
        elif "sender: window [" in lower_event:
            kind = "window"
        elif "frame" in lower_event and "sent" in lower_event:
            kind = "data_tx"
            elapsed_ms += transmission_delay
        elif "network: frame" in lower_event and "lost" in lower_event:
            kind = "data_lost"
        elif "network: ack" in lower_event and "lost" in lower_event:
            kind = "ack_lost"
        elif lower_event.startswith("timeout:"):
            kind = "timeout"
            elapsed_ms += timeout
        elif "retransmitting" in lower_event:
            kind = "retransmit"
        elif "window slides from" in lower_event:
            kind = "window_slide"
        elif "ack" in lower_event and "generated" in lower_event:
            kind = "ack_generated"
            elapsed_ms += ack_delay
        elif lower_event.startswith("sender: ack") and "received" in lower_event:
            kind = "ack_received"
        elif "out-of-order" in lower_event and "discard" in lower_event:
            kind = "discard"
        elif "duplicate" in lower_event and "discard" in lower_event:
            kind = "duplicate"
        elif "received and buffered" in lower_event:
            kind = "buffered"
        elif "received successfully" in lower_event or (
            "accepted" in lower_event and "frame" in lower_event
        ):
            kind = "received"
        elif "delivered to upper layer" in lower_event:
            kind = "delivered"
        elif "frame" in lower_event and "discard" in lower_event:
            kind = "discard"
        elif "ready to transmit" in lower_event:
            kind = "ready"
        else:
            kind = "info"

        if kind == "data_tx":
            status = "Retransmission" if attempt > 1 else "Data sent"
            frame_ack = f"Frame {frame}" if frame is not None else ""
        elif kind == "data_lost":
            status = "Packet loss"
            frame_ack = f"Frame {frame}" if frame is not None else ""
        elif kind == "ack_generated":
            status = "ACK generated"
            frame_ack = f"ACK {ack}" if ack is not None else ""
        elif kind == "ack_lost":
            status = "ACK loss"
            frame_ack = f"ACK {ack}" if ack is not None else ""
        elif kind == "ack_received":
            status = "Successful ACK"
            frame_ack = f"ACK {ack}" if ack is not None else ""
        elif kind == "timeout":
            status = "Timeout"
            frame_ack = f"Frame {frame}" if frame is not None else ""
            if ack is not None:
                frame_ack = f"ACK {ack}"
        elif kind == "retransmit":
            status = "Retransmission"
            frame_ack = ""
        elif kind in ("duplicate", "discard"):
            status = "Discarded frame"
            frame_ack = f"Frame {frame}" if frame is not None else ""
        elif kind in ("received", "delivered", "buffered"):
            status = "Frame received"
            frame_ack = f"Frame {frame}" if frame is not None else ""
        elif kind in ("window", "window_slide"):
            status = "Window update"
            frame_ack = ""
        elif kind == "complete":
            status = "Completed"
            frame_ack = ""
        elif kind == "start":
            status = "Started"
            frame_ack = ""
        else:
            status = "In progress"
            frame_ack = f"Frame {frame}" if frame is not None else (
                f"ACK {ack}" if ack is not None else ""
            )

        records.append({
            "step": len(records) + 1,
            "time_ms": elapsed_ms,
            "protocol": protocol,
            "event": event,
            "frame_ack": frame_ack,
            "status": status,
            "kind": kind,
            "frame": frame,
            "ack": ack,
            "attempt": attempt,
            "window": (
                (int(window_match.group(1)), int(window_match.group(2)))
                if window_match else None
            ),
            "slide": (
                (int(slide_match.group(1)), int(slide_match.group(2)))
                if slide_match else None
            ),
            "transmission_succeeded": None,
        })

    for index, record in enumerate(records):
        if record["kind"] == "data_tx":
            for following in records[index + 1:]:
                if following["kind"] == "data_tx" and (
                    following["frame"] == record["frame"]
                ):
                    break
                if following["kind"] == "data_lost" and (
                    following["frame"] == record["frame"]
                ):
                    record["transmission_succeeded"] = False
                    break
                if following["kind"] in (
                    "received", "buffered", "duplicate", "discard"
                ) and following["frame"] == record["frame"]:
                    record["transmission_succeeded"] = True
                    break
            if record["transmission_succeeded"] is None:
                record["transmission_succeeded"] = True
            if not record["transmission_succeeded"]:
                record["status"] = "Packet loss"

        elif record["kind"] == "ack_generated":
            for following in records[index + 1:]:
                if following["kind"] == "ack_generated":
                    break
                if following["kind"] == "ack_lost" and (
                    following["ack"] == record["ack"]
                ):
                    record["transmission_succeeded"] = False
                    record["status"] = "ACK loss"
                    break
                if following["kind"] == "ack_received" and (
                    following["ack"] == record["ack"]
                ):
                    record["transmission_succeeded"] = True
                    break
            if record["transmission_succeeded"] is None:
                record["transmission_succeeded"] = True

    return records


class AnimationPanel(ttk.Frame):
    """Animate actual protocol events on a scrollable time-ordered diagram."""

    COLORS = {
        "navy": "#14213D",
        "blue": "#2563EB",
        "green": "#16A34A",
        "red": "#DC2626",
        "orange": "#EA8A12",
        "grey": "#94A3B8",
        "light": "#F8FAFC",
        "grid": "#E2E8F0",
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="TFrame")

        self.header_canvas = tk.Canvas(
            self,
            height=90,
            bg="white",
            highlightthickness=1,
            highlightbackground="#D8E0EA",
        )
        self.header_canvas.pack(fill="x", padx=2, pady=(2, 0))

        timeline_frame = ttk.Frame(self)
        timeline_frame.pack(fill="both", expand=True, padx=2, pady=(0, 2))
        self.canvas = tk.Canvas(
            timeline_frame,
            height=35,
            bg="white",
            highlightthickness=1,
            highlightbackground="#D8E0EA",
        )
        self.scrollbar = ttk.Scrollbar(
            timeline_frame, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=(2, 0), pady=2)
        self.scrollbar.pack(side="right", fill="y", pady=2)

        self.records = []
        self.parameters = {}
        self.current_index = 0
        self.current_record = None
        self.on_event = None
        self.on_complete = None
        self.on_state = None
        self.playback_active = False
        self.paused = False
        self.step_mode = False
        self.after_id = None
        self.marker_ids = ()
        self.marker_x = 0.0
        self.marker_end_x = 0.0
        self.marker_direction = 1
        self.marker_steps = 0
        self.sender_base = 0
        self.receiver_base = 0
        self.received_frames = set()
        self.resize_pending = False

        self.canvas.bind("<Configure>", self._on_configure)
        self._draw_base()

    def _layout(self):
        width = max(self.canvas.winfo_width(), 720)
        sender_x = max(120, width * 0.19)
        receiver_x = min(width - 120, width * 0.81)
        return width, sender_x, receiver_x

    def _draw_base(self):
        self.header_canvas.delete("all")
        self.canvas.delete("all")
        width, sender_x, receiver_x = self._layout()
        self.sender_x = sender_x
        self.receiver_x = receiver_x
        self.row_start = 22
        self.row_gap = 42

        self.header_canvas.create_text(
            sender_x, 16, text="SENDER", fill=self.COLORS["navy"],
            font=("Segoe UI", 11, "bold")
        )
        self.header_canvas.create_text(
            receiver_x, 16, text="RECEIVER", fill=self.COLORS["navy"],
            font=("Segoe UI", 11, "bold")
        )
        self.header_canvas.create_rectangle(
            sender_x - 48, 26, sender_x + 48, 54,
            fill="#EFF6FF", outline="#93C5FD", width=1
        )
        self.header_canvas.create_rectangle(
            receiver_x - 48, 26, receiver_x + 48, 54,
            fill="#F0FDF4", outline="#86EFAC", width=1
        )
        self.header_canvas.create_text(
            sender_x, 40, text="Sender", fill=self.COLORS["navy"],
            font=("Segoe UI", 9, "bold")
        )
        self.header_canvas.create_text(
            receiver_x, 40, text="Receiver", fill=self.COLORS["navy"],
            font=("Segoe UI", 9, "bold")
        )
        self.current_status_id = self.header_canvas.create_text(
            width / 2, 66, text="Waiting for simulation",
            fill="#475569", font=("Segoe UI", 9, "bold")
        )
        self.window_status_id = self.header_canvas.create_text(
            width / 2, 82, text="Sender window: —    Receiver window: —",
            fill="#475569", font=("Segoe UI", 8)
        )
        self.header_canvas.create_line(
            sender_x, 54, sender_x, 90, fill="#CBD5E1", width=1
        )
        self.header_canvas.create_line(
            receiver_x, 54, receiver_x, 90, fill="#CBD5E1", width=1
        )
        self._update_scroll_region()

    def _on_configure(self, _event):
        if self.playback_active:
            self.resize_pending = True
            return
        self._redraw_history()

    def _redraw_history(self):
        current_index = self.current_index
        self._draw_base()
        if self.current_record is not None:
            self.header_canvas.itemconfigure(
                self.current_status_id,
                text=self._status_text(self.current_record),
                fill=self._status_color(self.current_record),
            )
        for index, record in enumerate(self.records[:current_index]):
            self._draw_event_row(record, index)
            self._draw_static_event(record, index)
        self._update_window_labels()
        self._update_scroll_region()
        if self.records and not self.playback_active:
            self._render_legend()
        self.resize_pending = False

    def _row_y(self, index):
        return self.row_start + index * self.row_gap

    def _update_scroll_region(self):
        width, _, _ = self._layout()
        row_count = max(self.current_index, len(self.records) if not self.playback_active else 0)
        content_bottom = self.row_start + row_count * self.row_gap + 70
        self.canvas.configure(
            scrollregion=(
                0, 0, width,
                max(self.canvas.winfo_height(), 150, content_bottom)
            )
        )

    def _scroll_to_event(self, index):
        self.canvas.update_idletasks()
        region = self.canvas.cget("scrollregion").split()
        if len(region) != 4:
            return
        content_height = float(region[3])
        viewport_height = max(self.canvas.winfo_height(), 1)
        target_top = max(
            0, self._row_y(index) - viewport_height / 2
        )
        self.canvas.yview_moveto(
            min(target_top / max(content_height, 1), 1)
        )

    def _update_window_labels(self):
        width, _, _ = self._layout()
        frame_count = int(self.parameters.get("frames", 0))
        window_size = int(self.parameters.get("window", 1))
        sender_end = min(self.sender_base + window_size - 1, frame_count - 1)
        receiver_end = min(self.receiver_base + window_size - 1, frame_count - 1)
        sender_window = (
            f"[{self.sender_base}, {sender_end}]"
            if frame_count and self.sender_base < frame_count else "[]"
        )
        receiver_window = (
            f"[{self.receiver_base}, {receiver_end}]"
            if frame_count and self.receiver_base < frame_count else "[]"
        )
        self.header_canvas.coords(self.window_status_id, width / 2, 82)
        self.header_canvas.itemconfigure(
            self.window_status_id,
            text=f"Sender window: {sender_window}    "
            f"Receiver window: {receiver_window}",
        )

    def _prepare_record(self, record):
        if record["kind"] == "window" and record["window"]:
            self.sender_base = record["window"][0]
        elif record["kind"] == "window_slide" and record["slide"]:
            self.sender_base = record["slide"][1]
        elif (
            record["kind"] == "data_tx"
            and record["attempt"] == 1
            and record["protocol"] == "One-Bit Sliding Window"
        ):
            self.sender_base = record["frame"] or 0
        elif (
            record["kind"] == "ack_received"
            and record["protocol"] == "One-Bit Sliding Window"
        ):
            self.sender_base += 1

        if record["kind"] == "received" and record["frame"] is not None:
            self.received_frames.add(record["frame"])
            while self.receiver_base in self.received_frames:
                self.receiver_base += 1
        elif record["kind"] == "buffered" and record["frame"] is not None:
            self.received_frames.add(record["frame"])
            while self.receiver_base in self.received_frames:
                self.receiver_base += 1

        self._update_window_labels()
        self.header_canvas.itemconfigure(
            self.current_status_id,
            text=self._status_text(record),
            fill=self._status_color(record),
        )

    @staticmethod
    def _status_text(record):
        kind = record["kind"]
        frame = record["frame"]
        ack = record["ack"]
        if kind == "start":
            message = "Simulation started"
        elif kind == "data_tx":
            action = "Retransmitting" if record["attempt"] > 1 else "Sending"
            message = f"{action} Frame {frame}"
        elif kind == "data_lost":
            message = f"Frame {frame} lost"
        elif kind == "ack_generated":
            message = f"Sending ACK {ack}"
        elif kind == "ack_lost":
            message = f"ACK {ack} lost"
        elif kind == "ack_received":
            message = f"ACK {ack} received"
        elif kind in ("received", "delivered"):
            message = f"Frame {frame} received"
        elif kind == "buffered":
            message = f"Frame {frame} buffered"
        elif kind in ("duplicate", "discard"):
            message = f"Frame {frame} discarded"
        elif kind == "timeout":
            message = "Timeout"
        elif kind == "retransmit":
            message = "Retransmission begins"
        elif kind == "window" and record["window"]:
            message = f"Sender window {record['window']}"
        elif kind == "window_slide" and record["slide"]:
            message = f"Sender window slides to {record['slide'][1]}"
        elif kind == "complete":
            message = "Simulation complete"
        else:
            message = record["event"]
        return f"Step {record['step']}: {message}"

    @staticmethod
    def _status_color(record):
        kind = record["kind"]
        if kind in ("data_lost", "ack_lost", "timeout"):
            return "#DC2626"
        if kind == "retransmit" or (
            kind == "data_tx" and record["attempt"] > 1
        ):
            return "#EA8A12"
        if kind in ("duplicate", "discard"):
            return "#64748B"
        if kind in ("received", "delivered", "buffered", "ack_received"):
            return "#16A34A"
        if kind in ("data_tx", "ack_generated"):
            return "#2563EB" if kind == "data_tx" else "#16A34A"
        return "#475569"

    def _draw_event_row(self, record, index):
        y = self._row_y(index)
        width, _, _ = self._layout()
        self.canvas.create_rectangle(
            0, y - 16, width, y + 16,
            fill="#EFF6FF" if index == self.current_index - 1 else "white",
            outline="",
            tags=("event_row",),
        )
        self.canvas.create_line(
            0, y + 17, width, y + 17,
            fill=self.COLORS["grid"], width=1
        )
        self.canvas.create_line(
            self.sender_x, 0, self.sender_x, y,
            fill="#CBD5E1", width=1
        )
        self.canvas.create_line(
            self.receiver_x, 0, self.receiver_x, y,
            fill="#CBD5E1", width=1
        )
        self.canvas.create_text(
            10, y, anchor="w",
            text=f"{record['step']:>3}  {record['time_ms']:>7.1f} ms",
            fill="#64748B", font=("Consolas", 7)
        )

    def _draw_static_event(self, record, index):
        y = self._row_y(index)
        kind = record["kind"]
        frame = record["frame"]
        ack = record["ack"]

        if kind == "data_tx":
            color = (
                self.COLORS["orange"] if record["attempt"] > 1
                else self.COLORS["blue"]
            )
            target_x = (
                self.sender_x + (self.receiver_x - self.sender_x) * 0.53
                if not record["transmission_succeeded"]
                else self.receiver_x
            )
            self._draw_arrow(
                self.sender_x, y - 5, target_x, y - 5, color,
                f"F{frame}", dashed=False,
                lost=not record["transmission_succeeded"],
            )
        elif kind == "ack_generated":
            target_x = (
                self.receiver_x - (self.receiver_x - self.sender_x) * 0.53
                if not record["transmission_succeeded"]
                else self.sender_x
            )
            self._draw_arrow(
                self.receiver_x, y + 5, target_x, y + 5,
                self.COLORS["green"], f"ACK {ack}", dashed=True,
                lost=not record["transmission_succeeded"],
            )
        elif kind in ("data_lost", "ack_lost"):
            text = f"✕  {'F' + str(frame) if frame is not None else 'ACK ' + str(ack)} LOST"
            self.canvas.create_text(
                (self.sender_x + self.receiver_x) / 2, y,
                text=text, fill=self.COLORS["red"],
                font=("Segoe UI", 8, "bold")
            )
        elif kind in ("received", "delivered", "buffered"):
            label = f"✓ F{frame}" if kind != "buffered" else f"Buffered F{frame}"
            self.canvas.create_text(
                self.receiver_x, y, text=label, fill=self.COLORS["green"],
                font=("Segoe UI", 8, "bold")
            )
        elif kind in ("duplicate", "discard"):
            self._draw_arrow(
                self.sender_x, y, self.receiver_x, y,
                self.COLORS["grey"], f"F{frame} discarded",
                dashed=True,
            )
        elif kind == "ack_received":
            self.canvas.create_text(
                self.sender_x, y, text=f"✓ ACK {ack}",
                fill=self.COLORS["green"], font=("Segoe UI", 8, "bold")
            )
        elif kind == "timeout":
            self.canvas.create_text(
                self.sender_x + 22, y, anchor="w",
                text="TIMEOUT", fill=self.COLORS["red"],
                font=("Segoe UI", 8, "bold")
            )
        elif kind == "retransmit":
            self.canvas.create_oval(
                self.sender_x - 5, y - 5, self.sender_x + 5, y + 5,
                fill=self.COLORS["orange"], outline=self.COLORS["orange"]
            )
        elif kind == "window":
            self.canvas.create_text(
                self.sender_x - 56, y, anchor="e",
                text=f"W {record['window']}", fill=self.COLORS["navy"],
                font=("Segoe UI", 7)
            )
        elif kind == "window_slide" and record["slide"]:
            self.canvas.create_text(
                self.sender_x - 10, y, anchor="e",
                text=f"Window → {record['slide'][1]}",
                fill=self.COLORS["navy"], font=("Segoe UI", 7)
            )
        elif kind in ("start", "complete"):
            self.canvas.create_text(
                (self.sender_x + self.receiver_x) / 2, y,
                text=(
                    "SIMULATION STARTED" if kind == "start"
                    else "SIMULATION COMPLETE"
                ),
                fill=self.COLORS["green"] if kind == "complete" else "#64748B",
                font=("Segoe UI", 7, "bold")
            )

    def _draw_arrow(
        self, start_x, y, end_x, end_y, color, label,
        dashed=False, lost=False
    ):
        self.canvas.create_line(
            start_x, y, end_x, end_y,
            fill=color, width=2,
            dash=(5, 3) if dashed else (),
            arrow=tk.LAST,
        )
        label_x = (start_x + end_x) / 2
        self.canvas.create_text(
            label_x, y - 10, text=label, fill=color,
            font=("Segoe UI", 8, "bold")
        )
        if lost:
            self.canvas.create_text(
                end_x, end_y, text="✕", fill=self.COLORS["red"],
                font=("Segoe UI", 13, "bold")
            )

    def _render_legend(self):
        y = self._row_y(max(self.current_index, 1)) + 25
        width, _, _ = self._layout()
        items = [
            ("Data frame", self.COLORS["blue"], False),
            ("ACK", self.COLORS["green"], True),
            ("Lost", self.COLORS["red"], False),
            ("Retransmit", self.COLORS["orange"], False),
            ("Discarded", self.COLORS["grey"], True),
            ("Received", self.COLORS["green"], False),
        ]
        total_width = min(width - 24, len(items) * 118)
        start = (width - total_width) / 2 + 8
        for index, (label, color, dashed) in enumerate(items):
            x = start + index * total_width / len(items)
            self.canvas.create_line(
                x, y + 21, x + 23, y + 21,
                fill=color, width=2, dash=(4, 3) if dashed else (),
                tags=("legend",)
            )
            self.canvas.create_text(
                x + 28, y + 21, anchor="w", text=label,
                fill="#334155", font=("Segoe UI", 7), tags=("legend",)
            )
        self.canvas.create_text(
            width / 2, y, text="LEGEND", fill=self.COLORS["navy"],
            font=("Segoe UI", 8, "bold"), tags=("legend",)
        )
        self._update_scroll_region()

    def play(
        self, events, protocol=None, parameters=None, on_event=None,
        on_complete=None, on_state=None
    ):
        self.reset()
        if protocol is None:
            source = "\n".join(events).lower()
            if "selective repeat" in source:
                protocol = "Selective Repeat"
            elif "go-back-n" in source:
                protocol = "Go-Back-N"
            else:
                protocol = "One-Bit Sliding Window"
        if parameters is None:
            frame_numbers = [
                int(match.group(1))
                for event in events
                for match in [_FRAME_PATTERN.search(event)]
                if match is not None
            ]
            parameters = {
                "frames": max(frame_numbers, default=0) + 1,
                "window": 1,
                "transmission": 1,
                "ack": 1,
                "timeout": 1,
            }
        self.records = normalize_events(events, protocol, parameters)
        self.parameters = parameters
        self.on_event = on_event
        self.on_complete = on_complete
        self.on_state = on_state
        self.playback_active = True
        self.paused = False
        self.step_mode = False
        self._update_window_labels()
        if self.on_state:
            self.on_state("Running")
        self._process_next()

    def reset(self):
        self._cancel_scheduled()
        self.records = []
        self.parameters = {}
        self.current_index = 0
        self.current_record = None
        self.playback_active = False
        self.paused = False
        self.step_mode = False
        self.marker_ids = ()
        self.sender_base = 0
        self.receiver_base = 0
        self.received_frames.clear()
        self.resize_pending = False
        self.on_event = None
        self.on_complete = None
        self.on_state = None
        self._draw_base()

    def pause(self):
        if not self.playback_active:
            return
        self.paused = True
        self._cancel_scheduled()
        self.header_canvas.itemconfigure(
            self.current_status_id, text="Paused"
        )
        if self.on_state:
            self.on_state("Paused")

    def resume(self):
        if not self.playback_active:
            return
        self.paused = False
        self.step_mode = False
        if self.on_state:
            self.on_state("Running")
        if self.marker_ids:
            self._animate_marker()
        else:
            self._schedule(0, self._process_next)

    def step_forward(self):
        if not self.playback_active:
            return
        self.paused = False
        self.step_mode = True
        if self.on_state:
            self.on_state("Stepping")
        if self.marker_ids:
            self._animate_marker()
        else:
            self._process_next()

    def _process_next(self):
        self.after_id = None
        if self.paused or not self.playback_active:
            return
        if self.current_index >= len(self.records):
            self._complete()
            return

        record = self.records[self.current_index]
        self.current_record = record
        self.current_index += 1
        if self.on_event:
            self.on_event(record)
        self._prepare_record(record)
        self._draw_event_row(record, self.current_index - 1)
        self._update_scroll_region()
        self._scroll_to_event(self.current_index - 1)

        if record["kind"] in ("data_tx", "ack_generated"):
            self._start_marker(record, self.current_index - 1)
        else:
            self._finish_current()

    def _start_marker(self, record, index):
        y = self._row_y(index)
        is_data = record["kind"] == "data_tx"
        start_x = self.sender_x if is_data else self.receiver_x
        end_x = self.receiver_x if is_data else self.sender_x
        failed = not record["transmission_succeeded"]
        if failed:
            progress = 0.53
            end_x = start_x + (end_x - start_x) * progress

        color = (
            self.COLORS["orange"]
            if is_data and record["attempt"] > 1
            else self.COLORS["blue"] if is_data
            else self.COLORS["green"]
        )
        label = f"F{record['frame']}" if is_data else f"ACK {record['ack']}"
        line_y = y - 5 if is_data else y + 5
        line = self.canvas.create_line(
            start_x, line_y, start_x, line_y,
            fill=color, width=2,
            dash=(5, 3) if not is_data else (),
            arrow=tk.LAST,
        )
        marker = self.canvas.create_oval(
            start_x - 12, line_y - 10, start_x + 12, line_y + 10,
            fill=color, outline=color,
        )
        text = self.canvas.create_text(
            start_x, line_y, text=label, fill="white",
            font=("Segoe UI", 7, "bold"),
        )
        self.marker_ids = (line, marker, text)
        self.marker_x = start_x
        self.marker_end_x = end_x
        self.marker_direction = 1 if end_x >= start_x else -1
        distance = abs(end_x - start_x)
        self.marker_steps = max(8, min(30, int(distance / 20)))
        self._animate_marker()

    def _animate_marker(self):
        if self.paused or not self.marker_ids:
            return
        line, marker, text = self.marker_ids
        self.marker_x += (
            self.marker_end_x - self.marker_x
        ) / max(self.marker_steps, 1)
        line_y = (
            self._row_y(self.current_index - 1) - 5
            if self.current_record["kind"] == "data_tx"
            else self._row_y(self.current_index - 1) + 5
        )
        self.canvas.coords(
            line, self.sender_x if self.marker_direction > 0 else self.receiver_x,
            line_y, self.marker_x, line_y
        )
        self.canvas.coords(
            marker, self.marker_x - 12, line_y - 10,
            self.marker_x + 12, line_y + 10
        )
        self.canvas.coords(text, self.marker_x, line_y)

        if abs(self.marker_end_x - self.marker_x) < 2:
            self.marker_x = self.marker_end_x
            self.canvas.coords(
                line,
                self.sender_x if self.marker_direction > 0 else self.receiver_x,
                line_y, self.marker_end_x, line_y
            )
            for item_id in self.marker_ids:
                self.canvas.delete(item_id)
            self.marker_ids = ()
            self._finish_current()
            return

        self.marker_steps -= 1
        self._schedule(16, self._animate_marker)

    def _finish_current(self):
        if self.resize_pending:
            self._redraw_history()
        else:
            self._draw_static_event(self.current_record, self.current_index - 1)
        self.marker_ids = ()
        if self.step_mode:
            self.paused = True
            self.header_canvas.itemconfigure(
                self.current_status_id,
                text=f"Paused after step {self.current_record['step']}"
            )
            if self.on_state:
                self.on_state("Paused")
            return
        self._schedule(120, self._process_next)

    def _complete(self):
        self.playback_active = False
        self.paused = False
        self.header_canvas.itemconfigure(
            self.current_status_id,
            text="Simulation complete",
            fill=self.COLORS["green"],
        )
        self._render_legend()
        if self.current_index:
            self._scroll_to_event(self.current_index - 1)
        if self.on_state:
            self.on_state("Completed")
        if self.on_complete:
            self.on_complete()

    def draw_network(self):
        """Retain the original redraw entry point for existing callers."""
        self._draw_base()

    def animate_next(self):
        """Retain the original event-advance entry point."""
        self._process_next()

    def animate_packet(self, event, is_ack=False):
        """Retain direct packet-animation calls from earlier panel clients."""
        protocol = (
            self.records[0]["protocol"]
            if self.records else "One-Bit Sliding Window"
        )
        parameters = self.parameters or {
            "frames": 1,
            "window": 1,
            "transmission": 1,
            "ack": 1,
            "timeout": 1,
        }
        records = normalize_events([event], protocol, parameters)
        if not records:
            return
        record = records[0]
        if is_ack:
            record["kind"] = "ack_generated"
            record["transmission_succeeded"] = True
        elif record["kind"] != "data_tx":
            return
        self.records.append(record)
        self.current_record = record
        self.current_index = len(self.records)
        self.playback_active = True
        self.paused = False
        self._draw_event_row(record, self.current_index - 1)
        self._start_marker(record, self.current_index - 1)

    def show_loss(self, event):
        """Retain the original loss-indicator entry point."""
        y = self._row_y(max(self.current_index - 1, 0))
        width, _, _ = self._layout()
        self.canvas.create_text(
            width / 2, y, text=f"✕ {event}",
            fill=self.COLORS["red"], font=("Segoe UI", 9, "bold")
        )

    def root_after(self, delay, callback):
        """Retain the original Tkinter scheduling helper."""
        return self.after(delay, callback)

    def _schedule(self, delay, callback):
        if self.paused or not self.playback_active:
            return
        self._cancel_scheduled()
        self.after_id = self.after(delay, callback)

    def _cancel_scheduled(self):
        if self.after_id is not None:
            try:
                self.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None
