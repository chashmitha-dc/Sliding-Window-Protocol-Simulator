
"""Simulation controller for all three ARQ protocols."""

from protocols.stop_and_wait import StopAndWaitProtocol
from protocols.go_back_n import GoBackNProtocol
from protocols.selective_repeat import SelectiveRepeatProtocol

from analysis.performance import calculate_performance


class Simulator:
    """Coordinate protocol selection and simulation execution."""

    def __init__(self):
        """Initialize all protocol implementations."""

        self.protocols = {
            "One-Bit Sliding Window": StopAndWaitProtocol(),
            "Go-Back-N": GoBackNProtocol(),
            "Selective Repeat": SelectiveRepeatProtocol()
        }

    def run_simulation(
        self,
        protocol_name,
        number_of_frames,
        window_size,
        transmission_delay,
        ack_delay,
        packet_loss,
        ack_loss,
        timeout,
        seed=None
    ):
        """Run the selected protocol and calculate performance."""

        # --------------------------------
        # INPUT VALIDATION
        # --------------------------------

        if protocol_name not in self.protocols:
            raise ValueError("Please select a valid protocol.")

        if number_of_frames < 1:
            raise ValueError("Number of frames must be at least 1.")

        if window_size < 1:
            raise ValueError("Window size must be at least 1.")

        if transmission_delay <= 0:
            raise ValueError("Transmission delay must be positive.")

        if ack_delay < 0:
            raise ValueError("ACK delay cannot be negative.")

        if timeout <= 0:
            raise ValueError("Timeout must be positive.")

        if not 0 <= packet_loss <= 100:
            raise ValueError(
                "Packet loss must be between 0 and 100."
            )

        if not 0 <= ack_loss <= 100:
            raise ValueError(
                "ACK loss must be between 0 and 100."
            )

        # --------------------------------
        # SELECT PROTOCOL
        # --------------------------------

        selected_protocol = self.protocols[protocol_name]

        # --------------------------------
        # EXECUTE STOP-AND-WAIT
        # --------------------------------

        if protocol_name == "One-Bit Sliding Window":

            results = selected_protocol.simulate(
                number_of_frames=number_of_frames,
                transmission_delay=transmission_delay,
                ack_delay=ack_delay,
                packet_loss=packet_loss,
                ack_loss=ack_loss,
                timeout=timeout,
                seed=seed
            )

        # --------------------------------
        # EXECUTE GO-BACK-N / SELECTIVE REPEAT
        # --------------------------------

        else:

            results = selected_protocol.simulate(
                number_of_frames=number_of_frames,
                window_size=window_size,
                transmission_delay=transmission_delay,
                ack_delay=ack_delay,
                packet_loss=packet_loss,
                ack_loss=ack_loss,
                timeout=timeout,
                seed=seed
            )

        # --------------------------------
        # DELIVERED FRAME COUNT
        # --------------------------------

        # Preserve the value returned by the protocol.
        # If an older protocol implementation does not yet
        # return it, use the requested frame count as fallback.

        results.setdefault(
            "delivered_frames",
            number_of_frames
        )

        # --------------------------------
        # CALCULATE PERFORMANCE
        # --------------------------------

        performance = calculate_performance(
            results,
            number_of_frames
        )

        results.update(performance)

        return results
