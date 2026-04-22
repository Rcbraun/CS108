import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

SR = 44100  # samples per second — standard CD quality

# ── Playback ──────────────────────────────────────────────────────────────────
def play(wave):
    """Play a numpy array as audio."""
    sd.play(wave.astype(np.float32), SR)
    sd.wait()

# ── Save ─────────────────────────────────────────────────────────────────────
def save(wave, filename):
    """Save a numpy array as a 16-bit WAV file."""
    normalized = np.int16(wave / np.max(np.abs(wave)) * 32767)
    write(filename, SR, normalized)
    print(f"Saved: {filename}")

# ── Visualize ─────────────────────────────────────────────────────────────────
def show(wave, title="", duration=0.05):
    """Plot the first `duration` seconds of a wave."""
    samples = int(SR * duration)
    plt.figure(figsize=(10, 2))
    plt.plot(wave[:samples], linewidth=0.8)
    plt.title(title)
    plt.xlabel("samples")
    plt.ylabel("amplitude")
    plt.tight_layout()
    plt.show()

# ── Time axis ─────────────────────────────────────────────────────────────────
def timeline(duration):
    """Return a time array for a given duration in seconds."""
    return np.linspace(0, duration, int(SR * duration))

# ── Sine ──────────────────────────────────────────────────────────────────────
def sine(freq, duration, amplitude=0.3):
    t = timeline(duration)
    return amplitude * np.sin(2 * np.pi * freq * t)
