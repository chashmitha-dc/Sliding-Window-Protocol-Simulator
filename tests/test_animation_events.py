"""Tests for converting real protocol output into animation events."""

import unittest

from gui.animation_panel import normalize_events
from simulation.simulator import Simulator


PROTOCOLS = (
    "One-Bit Sliding Window",
    "Go-Back-N",
    "Selective Repeat",
)


class AnimationEventNormalizationTests(unittest.TestCase):
    def setUp(self):
        self.simulator = Simulator()

    def _run_and_check(self, protocol, window, packet_loss, ack_loss):
        parameters = {
            "frames": 20,
            "window": window,
            "transmission": 10,
            "ack": 5,
            "packet_loss": packet_loss,
            "ack_loss": ack_loss,
            "timeout": 50,
        }
        results = self.simulator.run_simulation(
            protocol_name=protocol,
            number_of_frames=parameters["frames"],
            window_size=window,
            transmission_delay=parameters["transmission"],
            ack_delay=parameters["ack"],
            packet_loss=packet_loss,
            ack_loss=ack_loss,
            timeout=parameters["timeout"],
            seed=202 if packet_loss else 303 if ack_loss else 101,
        )
        records = normalize_events(results["events"], protocol, parameters)
        source_events = [
            event.strip() for event in results["events"] if event.strip()
        ]

        self.assertEqual(
            [record["event"] for record in records],
            source_events,
        )
        self.assertEqual(
            [record["step"] for record in records],
            list(range(1, len(records) + 1)),
        )
        self.assertEqual(
            [record["time_ms"] for record in records],
            sorted(record["time_ms"] for record in records),
        )
        self.assertEqual(
            sum(record["kind"] == "data_lost" for record in records),
            results["packets_lost"],
        )
        self.assertEqual(
            sum(
                record["kind"] == "data_tx"
                and not record["transmission_succeeded"]
                for record in records
            ),
            results["packets_lost"],
        )
        self.assertEqual(
            sum(
                record["kind"] == "data_tx" and record["attempt"] > 1
                for record in records
            ),
            results["retransmissions"],
        )
        self.assertEqual(
            sum(record["kind"] == "ack_lost" for record in records),
            sum("Network: ACK " in event and " LOST" in event for event in source_events),
        )
        self.assertEqual(records[0]["kind"], "start")
        self.assertEqual(records[-1]["kind"], "complete")
        return records, results

    def test_ideal_network_for_each_protocol(self):
        for protocol in PROTOCOLS:
            with self.subTest(protocol=protocol):
                records, results = self._run_and_check(protocol, 4, 0, 0)
                self.assertEqual(results["delivered_frames"], 20)
                self.assertEqual(results["retransmissions"], 0)
                self.assertFalse(any(
                    record["kind"] in ("data_lost", "ack_lost")
                    for record in records
                ))

    def test_packet_loss_for_each_protocol(self):
        for protocol in PROTOCOLS:
            with self.subTest(protocol=protocol):
                records, results = self._run_and_check(protocol, 4, 20, 0)
                self.assertGreater(results["packets_lost"], 0)
                self.assertGreater(results["retransmissions"], 0)

    def test_ack_loss_for_each_protocol(self):
        for protocol in PROTOCOLS:
            with self.subTest(protocol=protocol):
                records, results = self._run_and_check(protocol, 4, 0, 20)
                self.assertGreater(
                    sum(record["kind"] == "ack_lost" for record in records),
                    0,
                )
                self.assertGreater(results["retransmissions"], 0)
                if protocol == "One-Bit Sliding Window":
                    self.assertTrue(any(
                        record["kind"] == "duplicate"
                        for record in records
                    ))

    def test_window_sizes_for_each_sliding_window_protocol(self):
        for protocol in PROTOCOLS:
            for window in (1, 4, 7):
                with self.subTest(protocol=protocol, window=window):
                    records, results = self._run_and_check(
                        protocol, window, 0, 0
                    )
                    self.assertEqual(results["delivered_frames"], 20)
                    self.assertTrue(all(
                        record["window"] is None
                        or record["window"][0] <= record["window"][1]
                        for record in records
                    ))

    def test_protocol_specific_receive_semantics_are_preserved(self):
        gbn_records, _ = self._run_and_check("Go-Back-N", 4, 20, 0)
        sr_records, _ = self._run_and_check("Selective Repeat", 4, 20, 0)
        self.assertTrue(any(
            record["kind"] == "discard" for record in gbn_records
        ))
        self.assertTrue(any(
            record["kind"] == "buffered" for record in sr_records
        ))


if __name__ == "__main__":
    unittest.main()
