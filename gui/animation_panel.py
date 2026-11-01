
"""Animated Sender-Receiver panel for ARQ protocol simulation."""

import tkinter as tk
from tkinter import ttk


class AnimationPanel(ttk.Frame):
    """Display animated frame and acknowledgement transmission."""

    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(
            self,
            height=260,
            bg="#F8FAFC",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

        self.sender_x = 100
        self.receiver_x = 650
        self.center_y = 120

        self.animation_speed = 15
        self.animation_delay = 20

        self.current_animation = 0
        self.animation_queue = []
        self.running = False

        self.draw_network()

    def draw_network(self):
        """Draw sender, receiver and communication channel."""

        self.canvas.delete("all")

        width = max(self.canvas.winfo_width(), 750)
        self.sender_x = 100
        self.receiver_x = width - 100

        self.canvas.create_text(
            self.sender_x,
            35,
            text="SENDER",
            font=("Segoe UI", 15, "bold"),
            fill="#14213D"
        )

        self.canvas.create_text(
            self.receiver_x,
            35,
            text="RECEIVER",
            font=("Segoe UI", 15, "bold"),
            fill="#14213D"
        )

        self.canvas.create_rectangle(
            self.sender_x - 45,
            65,
            self.sender_x + 45,
            105,
            fill="#DBEAFE",
            outline="#2563EB",
            width=2
        )

        self.canvas.create_rectangle(
            self.receiver_x - 45,
            65,
            self.receiver_x + 45,
            105,
            fill="#DCFCE7",
            outline="#16A34A",
            width=2
        )

        self.canvas.create_text(
            self.sender_x,
            85,
            text="Sender",
            font=("Segoe UI", 10, "bold")
        )

        self.canvas.create_text(
            self.receiver_x,
            85,
            text="Receiver",
            font=("Segoe UI", 10, "bold")
        )

        # Data transmission lane
        self.canvas.create_line(
            self.sender_x + 50,
            130,
            self.receiver_x - 50,
            130,
            fill="#64748B",
            width=2,
            arrow=tk.LAST
        )

        self.canvas.create_text(
            (self.sender_x + self.receiver_x) / 2,
            110,
            text="DATA FRAMES",
            fill="#2563EB",
            font=("Segoe UI", 9, "bold")
        )

        # ACK transmission lane
        self.canvas.create_line(
            self.receiver_x - 50,
            205,
            self.sender_x + 50,
            205,
            fill="#64748B",
            width=2,
            arrow=tk.LAST
        )

        self.canvas.create_text(
            (self.sender_x + self.receiver_x) / 2,
            225,
            text="ACKNOWLEDGEMENTS",
            fill="#16A34A",
            font=("Segoe UI", 9, "bold")
        )

        self.canvas.create_text(
            self.sender_x,
            155,
            text="Waiting",
            fill="#64748B",
            tags="sender_status"
        )

        self.canvas.create_text(
            self.receiver_x,
            155,
            text="Waiting",
            fill="#64748B",
            tags="receiver_status"
        )

    def reset(self):
        """Stop current animation and reset the network."""

        self.running = False
        self.animation_queue.clear()
        self.current_animation = 0

        self.draw_network()

    def play(self, events):
        """Play protocol events as frame and ACK animations."""

        self.reset()

        self.animation_queue = list(events)
        self.running = True

        self.animate_next()

    def animate_next(self):
        """Process the next event in the animation queue."""

        if not self.running:
            return

        if not self.animation_queue:
            self.running = False

            self.canvas.create_text(
                (self.sender_x + self.receiver_x) / 2,
                250,
                text="SIMULATION COMPLETED",
                fill="#16A34A",
                font=("Segoe UI", 10, "bold")
            )
            return

        event = self.animation_queue.pop(0)

        if "Frame" in event and "sent" in event:
            self.animate_packet(event, is_ack=False)

        elif "ACK" in event and "received" in event:
            self.animate_packet(event, is_ack=True)

        elif "LOST" in event:
            self.show_loss(event)

        elif "accepted" in event or "received successfully" in event:
            self.canvas.itemconfig(
                "receiver_status",
                text="Frame received",
                fill="#16A34A"
            )
            self.root_after(self.animation_delay, self.animate_next)

        else:
            self.root_after(5, self.animate_next)

    def animate_packet(self, event, is_ack=False):
        """Animate one data frame or acknowledgement."""

        if is_ack:
            start_x = self.receiver_x - 50
            end_x = self.sender_x + 50
            y = 205
            color = "#16A34A"
            label = "ACK"
            self.canvas.itemconfig(
                "sender_status",
                text="Receiving ACK",
                fill="#16A34A"
            )
        else:
            start_x = self.sender_x + 50
            end_x = self.receiver_x - 50
            y = 130
            color = "#2563EB"
            label = event.split(" sent")[0].split(":")[-1].strip()

            self.canvas.itemconfig(
                "sender_status",
                text="Sending Frame",
                fill="#2563EB"
            )

        packet = self.canvas.create_rectangle(
            start_x - 25,
            y - 14,
            start_x + 25,
            y + 14,
            fill=color,
            outline=color
        )

        text = self.canvas.create_text(
            start_x,
            y,
            text=label,
            fill="white",
            font=("Segoe UI", 8, "bold")
        )

        def move():
            if not self.running:
                return

            coords = self.canvas.coords(packet)

            if not coords:
                return

            current_x = (coords[0] + coords[2]) / 2

            if abs(end_x - current_x) <= self.animation_speed:
                self.canvas.coords(
                    packet,
                    end_x - 25, y - 14,
                    end_x + 25, y + 14
                )
                self.canvas.coords(text, end_x, y)

                self.canvas.delete(packet)
                self.canvas.delete(text)

                if is_ack:
                    self.canvas.itemconfig(
                        "sender_status",
                        text="ACK received",
                        fill="#16A34A"
                    )
                else:
                    self.canvas.itemconfig(
                        "receiver_status",
                        text="Frame delivered",
                        fill="#16A34A"
                    )

                self.root_after(
                    self.animation_delay,
                    self.animate_next
                )

                return

            direction = self.animation_speed if end_x > current_x else -self.animation_speed

            self.canvas.move(packet, direction, 0)
            self.canvas.move(text, direction, 0)

            self.root_after(15, move)

        move()

    def show_loss(self, event):
        """Display a lost packet or ACK."""

        self.canvas.itemconfig(
            "receiver_status",
            text="Packet / ACK lost",
            fill="#DC2626"
        )

        self.canvas.create_text(
            (self.sender_x + self.receiver_x) / 2,
            175,
            text="✕ LOST",
            fill="#DC2626",
            font=("Segoe UI", 12, "bold")
        )

        self.root_after(
            500,
            self.animate_next
        )

    def root_after(self, delay, callback):
        """Schedule an animation callback safely."""

        self.after(delay, callback)
