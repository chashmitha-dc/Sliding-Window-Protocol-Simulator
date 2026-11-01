
"""Performance calculations for ARQ protocol simulations."""


def calculate_performance(results, number_of_frames):
    """Calculate throughput and transmission efficiency."""

    total_transmitted = results["total_frames_transmitted"]
    total_time = results["total_time_ms"]

    delivered_frames = results.get(
        "delivered_frames",
        number_of_frames
    )

    # Throughput in frames per second
    if total_time <= 0:
        throughput = 0.0
    else:
        throughput = delivered_frames / (total_time / 1000)

    # Transmission efficiency in percentage
    if total_transmitted <= 0:
        efficiency = 0.0
    else:
        efficiency = (
            delivered_frames / total_transmitted
        ) * 100

    return {
        "throughput_fps": round(throughput, 2),
        "efficiency_percent": round(efficiency, 2)
    }
