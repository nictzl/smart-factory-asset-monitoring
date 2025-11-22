import numpy as np
from collections import deque

def compute_vibration_rms(value: float) -> float:
    return np.sqrt(value**2)

window = deque(maxlen=5)

def compute_temp_moving_avg(temp: float) -> float:
    window.append(temp)
    return sum(window) / len(window)
