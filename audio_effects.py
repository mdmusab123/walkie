import numpy as np
from scipy.signal import butter, lfilter

# Apply low-pass filter to mimic muffled walkie-talkie sound
def low_pass_filter(data, rate, cutoff=3000, order=6):
    nyquist = 0.5 * rate
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

# Add white noise to simulate static
def add_static(data, noise_factor=0.005):
    noise = np.random.normal(0, 1, data.shape)
    return data + noise_factor * noise

# Combine both effects (low-pass filter and static)
def apply_walkie_talkie_effect(data, rate):
    filtered = low_pass_filter(data, rate)
    with_static = add_static(filtered)
    return np.clip(with_static, -1, 1)  # Ensure the values are in the valid range
