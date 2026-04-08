def detect_behavioral_instability(metrics):

    flags = []

    # Volatility threshold
    if metrics["mean_volatility"] > 1_000_000:
        flags.append("High Volatility")

    # Oscillation proxy (CV)
    if metrics["cv_allocation"] > 0.15:
        flags.append("Oscillatory Behavior")

    # Combined instability
    if (
        metrics["mean_volatility"] > 800_000 and
        metrics["cv_allocation"] > 0.12
    ):
        flags.append("System Instability Detected")

    return flags