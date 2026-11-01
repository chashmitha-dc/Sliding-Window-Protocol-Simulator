
"""One-Bit Sliding Window (Stop-and-Wait ARQ) implementation."""

import random


class StopAndWaitProtocol:
    """Simulate Stop-and-Wait ARQ with packet and ACK loss."""

    MAX_ATTEMPTS = 1000

    def simulate(
        self,
        number_of_frames,
        transmission_delay,
        ack_delay,
        packet_loss,
        ack_loss,
        timeout,
        seed=None
    ):
        # --------------------------------
        # INPUT VALIDATION
        # --------------------------------

        if number_of_frames < 1:
            raise ValueError("Number of frames must be at least 1.")

        if transmission_delay <= 0:
            raise ValueError("Transmission delay must be positive.")

        if ack_delay < 0:
            raise ValueError("ACK delay cannot be negative.")

        if timeout <= 0:
            raise ValueError("Timeout must be positive.")

        if not 0 <= packet_loss <= 100:
            raise ValueError("Packet loss must be between 0 and 100.")

        if not 0 <= ack_loss <= 100:
            raise ValueError("ACK loss must be between 0 and 100.")

        rng = random.Random(seed)

        # --------------------------------
        # PERFORMANCE COUNTERS
        # --------------------------------

        total_transmitted = 0
        retransmissions = 0
        packets_lost = 0
        acks_received = 0
        total_time = 0
        delivered_frames = 0

        # --------------------------------
        # SENDER AND RECEIVER STATE
        # --------------------------------

        sender_sequence = 0
        receiver_expected = 0

        events = []

        events.append("Stop-and-Wait ARQ simulation started.")

        # --------------------------------
        # TRANSMIT EACH FRAME
        # --------------------------------

        for frame in range(number_of_frames):

            attempt = 0

            while True:

                attempt += 1

                if attempt > self.MAX_ATTEMPTS:
                    raise RuntimeError(
                        f"Frame {frame} exceeded maximum retry limit."
                    )

                total_transmitted += 1

                if attempt > 1:
                    retransmissions += 1

                events.append(
                    f"\nSender: Frame {frame}, "
                    f"Sequence {sender_sequence} sent "
                    f"(Attempt {attempt})"
                )

                total_time += transmission_delay

                # --------------------------------
                # CHECK DATA PACKET LOSS
                # --------------------------------

                if rng.random() < packet_loss / 100:

                    packets_lost += 1

                    events.append(
                        f"Network: Frame {frame} LOST"
                    )

                    events.append(
                        f"Timeout: Waiting for retransmission of Frame {frame}"
                    )

                    total_time += timeout

                    continue

                # --------------------------------
                # RECEIVER CHECKS SEQUENCE NUMBER
                # --------------------------------

                if sender_sequence == receiver_expected:

                    events.append(
                        f"Receiver: Frame {frame} received successfully"
                    )

                    events.append(
                        f"Receiver: Frame {frame} delivered to upper layer"
                    )

                    delivered_frames += 1

                    # Expect the other sequence number next
                    receiver_expected = 1 - receiver_expected

                else:

                    events.append(
                        f"Receiver: Duplicate Frame {frame} detected and discarded"
                    )

                # --------------------------------
                # RECEIVER GENERATES ACK
                # --------------------------------

                ack_number = sender_sequence

                events.append(
                    f"Receiver: ACK {ack_number} generated"
                )

                total_time += ack_delay

                # --------------------------------
                # CHECK ACK LOSS
                # --------------------------------

                if rng.random() < ack_loss / 100:

                    events.append(
                        f"Network: ACK {ack_number} LOST"
                    )

                    events.append(
                        f"Timeout: Sender is waiting for ACK {ack_number}"
                    )

                    total_time += timeout

                    continue

                # --------------------------------
                # ACK SUCCESSFULLY RECEIVED
                # --------------------------------

                acks_received += 1

                events.append(
                    f"Sender: ACK {ack_number} received"
                )

                # Move to the next sequence number
                sender_sequence = 1 - sender_sequence

                events.append(
                    f"Sender: Ready to transmit next frame"
                )

                break

        events.append(
            "\nStop-and-Wait ARQ simulation completed."
        )

        # --------------------------------
        # RETURN RESULTS
        # --------------------------------

        return {
            "total_frames_transmitted": total_transmitted,
            "retransmissions": retransmissions,
            "packets_lost": packets_lost,
            "acks_received": acks_received,
            "delivered_frames": delivered_frames,
            "total_time_ms": total_time,
            "events": events
        }
