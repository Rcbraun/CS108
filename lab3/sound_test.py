import sounddevice as sd
import numpy as np

SR = 44100  # sample rate: 44100 samples per second
t = np.linspace(0, 1, SR)
wave = 0.3 * np.sin(2 * np.pi * 440 * t)
sd.play(wave, SR)
sd.wait()