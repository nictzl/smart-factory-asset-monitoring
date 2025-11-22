def compute_anomaly_score(value: float, mean: float = 0.5, std: float = 0.2):
    return (value - mean) / std
