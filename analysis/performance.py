
"""Performance calculations for ARQ protocol simulations."""


def calculate_performance(results, number_of_frames):
    """Calculate throughput, efficiency, and retransmission metrics.

    Throughput is based on successfully delivered frames over the simulated
    transmission time. Efficiency is the percentage of successfully delivered
    frames relative to all transmitted frames. Retransmissions are calculated as
    the difference between total transmissions and the original frame count.
    """

    total_transmitted = int(results.get("total_frames_transmitted", 0))
    total_time_ms = float(results.get("total_time_ms", 0))

    delivered_frames = int(
        results.get("delivered_frames", min(number_of_frames, total_transmitted))
    )

    if delivered_frames < 0:
        delivered_frames = 0

    if total_time_ms <= 0:
        throughput = 0.0
    else:
        throughput = delivered_frames / (total_time_ms / 1000.0)

    if total_transmitted <= 0:
        efficiency = 0.0
    else:
        efficiency = (delivered_frames / total_transmitted) * 100

    retransmissions = max(total_transmitted - number_of_frames, 0)

    return {
        "delivered_frames": delivered_frames,
        "retransmissions": retransmissions,
        "throughput_fps": round(throughput, 2),
        "efficiency_percent": round(efficiency, 2),
    }
