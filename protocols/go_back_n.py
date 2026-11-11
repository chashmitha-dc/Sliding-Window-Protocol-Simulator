
"""Go-Back-N ARQ protocol implementation."""

import random


class GoBackNProtocol:
    """Simulate Go-Back-N ARQ with packet loss, ACK loss and timeout."""

    MAX_ATTEMPTS = 1000

    def simulate(
        self,
        number_of_frames,
        window_size,
        transmission_delay,
        ack_delay,
        packet_loss,
        ack_loss,
        timeout,
        seed=None
    ):
        # -------------------------------
        # INPUT VALIDATION
        # -------------------------------

        if number_of_frames < 0:
            raise ValueError("Number of frames cannot be negative.")

        if window_size < 1:
            raise ValueError("Window size must be at least 1.")

        if transmission_delay <= 0 or ack_delay < 0:
            raise ValueError("Invalid transmission or ACK delay.")

        if timeout <= 0:
            raise ValueError("Timeout must be positive.")

        if not 0 <= packet_loss <= 100:
            raise ValueError("Packet loss must be between 0 and 100.")

        if not 0 <= ack_loss <= 100:
            raise ValueError("ACK loss must be between 0 and 100.")

        rng = random.Random(seed)

        # -------------------------------
        # PERFORMANCE COUNTERS
        # -------------------------------

        total_transmitted = 0
        retransmissions = 0
        packets_lost = 0
        acks_received = 0
        total_time = 0
        delivered_frames = 0

        # -------------------------------
        # SENDER AND RECEIVER STATE
        # -------------------------------

        base = 0
        receiver_expected = 0

        attempts = [0] * number_of_frames

        events = []

        events.append("Go-Back-N simulation started.")

        # -------------------------------
        # MAIN SIMULATION LOOP
        # -------------------------------

        while base < number_of_frames:

            window_end = min(
                base + window_size,
                number_of_frames
            )

            events.append(
                f"\nSender: Window [{base}, {window_end - 1}]"
            )

            highest_ack_received = base - 1

            # Send all frames in the current window
            for frame in range(base, window_end):

                attempts[frame] += 1

                if attempts[frame] > self.MAX_ATTEMPTS:
                    raise RuntimeError(
                        f"Frame {frame} exceeded maximum retry limit."
                    )

                total_transmitted += 1

                if attempts[frame] > 1:
                    retransmissions += 1

                events.append(
                    f"Sender: Frame {frame} sent "
                    f"(Attempt {attempts[frame]})"
                )

                total_time += transmission_delay

                # -------------------------------
                # PACKET LOSS
                # -------------------------------

                if rng.random() < packet_loss / 100:

                    packets_lost += 1

                    events.append(
                        f"Network: Frame {frame} LOST"
                    )

                    continue

                # -------------------------------
                # RECEIVER PROCESSING
                # -------------------------------

                if frame == receiver_expected:

                    delivered_frames += 1
                    events.append(
                        f"Receiver: Frame {frame} accepted"
                    )

                    receiver_expected += 1

                elif frame < receiver_expected:

                    events.append(
                        f"Receiver: Duplicate Frame {frame} discarded"
                    )

                else:

                    events.append(
                        f"Receiver: Out-of-order Frame {frame} discarded"
                    )

                # -------------------------------
                # CUMULATIVE ACK GENERATION
                # -------------------------------

                ack_number = receiver_expected - 1

                events.append(
                    f"Receiver: Cumulative ACK {ack_number} generated"
                )

                total_time += ack_delay

                # -------------------------------
                # ACK LOSS
                # -------------------------------

                if rng.random() < ack_loss / 100:

                    events.append(
                        f"Network: ACK {ack_number} LOST"
                    )

                else:

                    acks_received += 1

                    events.append(
                        f"Sender: ACK {ack_number} received"
                    )

                    highest_ack_received = max(
                        highest_ack_received,
                        ack_number
                    )

            # -------------------------------
            # SLIDE SENDER WINDOW
            # -------------------------------

            if highest_ack_received >= base:

                old_base = base

                base = highest_ack_received + 1

                events.append(
                    f"Sender: Window slides from "
                    f"{old_base} to {base}"
                )

            else:

                events.append(
                    "Timeout: No new cumulative ACK received."
                )

                events.append(
                    "Sender: Retransmitting outstanding window."
                )

                total_time += timeout

        events.append("\nGo-Back-N simulation completed.")

        # -------------------------------
        # RETURN RESULTS
        # -------------------------------

        return {
            "total_frames_transmitted": total_transmitted,
            "retransmissions": retransmissions,
            "packets_lost": packets_lost,
            "acks_received": acks_received,
            "delivered_frames": delivered_frames,
            "total_time_ms": total_time,
            "events": events
        }
