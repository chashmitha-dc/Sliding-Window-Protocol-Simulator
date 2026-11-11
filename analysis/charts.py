"""Helper utilities for performance chart generation."""


def protocol_names(results):
    """Return ordered protocol names from a comparison dictionary."""
    return list(results.keys())


def metric_series(results, metric_key):
    """Extract a metric series for each protocol in a results dictionary."""
    return [float(results[name].get(metric_key, 0.0)) for name in protocol_names(results)]
