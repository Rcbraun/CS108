from sound_base import *

# tone = sine(440, 2.0)   # 440 Hz = the note A4 (concert pitch)
# show(tone, "440 Hz sine wave")
# play(tone)

# for freq in [220, 440, 880, 1760]:
#     print(f"Playing {freq} Hz")
#     play(sine(freq, 1.0))

# freq = 440
# dur  = 1.5
# t    = timeline(dur)

# sine_wave     = 0.3 * np.sin(2 * np.pi * freq * t)
# square_wave   = 0.3 * np.sign(np.sin(2 * np.pi * freq * t))
# sawtooth_wave = 0.3 * (2 * (t * freq % 1) - 1)
# triangle_wave = 0.3 * (2 * np.abs(2 * (t * freq % 1) - 1) - 1)

# for wave, name in [
#     (sine_wave,     "sine"),
#     (square_wave,   "square"),
#     (sawtooth_wave, "sawtooth"),
#     (triangle_wave, "triangle"),
# ]:
#     show(wave, name)
#     play(wave)

# def harmonic_tone(freq, duration, num_harmonics=6):
#     t = timeline(duration)
#     wave = np.zeros(len(t))
#     for n in range(1, num_harmonics + 1):
#         amplitude = 1.0 / n          # each harmonic is quieter
#         wave += amplitude * np.sin(2 * np.pi * freq * n * t)
#     wave *= 0.3 / np.max(np.abs(wave))  # normalize
#     return wave

# plain    = sine(440, 2.0)
# rich     = harmonic_tone(440, 2.0, num_harmonics=6)
# very_rich = harmonic_tone(440, 2.0, num_harmonics=20)

# play(plain)
# play(rich)
# play(very_rich)

def adsr(duration, attack=0.01, decay=0.1, sustain=0.7, release=0.1):
    """Return an ADSR envelope as a numpy array."""
    n = int(SR * duration)
    env = np.zeros(n)

    a = int(SR * attack)
    d = int(SR * decay)
    r = int(SR * release)
    s = n - a - d - r

    env[:a]         = np.linspace(0, 1, a)           # attack
    env[a:a+d]      = np.linspace(1, sustain, d)      # decay
    env[a+d:a+d+s]  = sustain                         # sustain
    env[a+d+s:]     = np.linspace(sustain, 0, r)      # release

    return env

# t    = timeline(2.0)
# tone = 0.5 * np.sin(2 * np.pi * 440 * t)

# abrupt   = tone
# shaped   = tone * adsr(2.0, attack=0.01, release=0.1)
# piano_like = tone * adsr(2.0, attack=0.005, decay=0.3, sustain=0.3, release=0.4)
# pad_like   = tone * adsr(2.0, attack=0.6,  decay=0.1, sustain=0.9, release=0.5)

# for wave, name in [
#     (abrupt,     "abrupt (no envelope)"),
#     (shaped,     "basic envelope"),
#     (piano_like, "piano-like"),
#     (pad_like,   "slow pad"),
# ]:
#     show(wave, name, duration=2.0)
#     play(wave)

def note(freq, duration, amplitude=0.3, waveform='sine'):
    t = timeline(duration)
    if waveform == 'sine':
        wave = np.sin(2 * np.pi * freq * t)
    elif waveform == 'sawtooth':
        wave = 2 * (t * freq % 1) - 1
    elif waveform == 'square':
        wave = np.sign(np.sin(2 * np.pi * freq * t))

    env = adsr(duration, attack=0.02, decay=0.1, sustain=0.6, release=0.15)
    return amplitude * wave * env

def semitones(base_freq, steps):
    """Shift a frequency by `steps` semitones."""
    return base_freq * (2 ** (steps / 12))

# A minor scale starting at A3 (220 Hz)
# Steps: 0, 2, 3, 5, 7, 8, 10, 12
A3 = 220.0
scale_steps = [0, 2, 3, 5, 7, 8, 10, 12]

melody = np.concatenate([
    note(semitones(A3, s), 0.4) for s in scale_steps
])
# play(melody)
# save(melody, "scale.wav")
# play(np.concatenate([note(semitones(A3, s), 0.4) for s in reversed(scale_steps)]))

def chord(freqs, duration, amplitude=0.25):
    waves = [note(f, duration, amplitude) for f in freqs]
    mixed = sum(waves)
    return mixed / np.max(np.abs(mixed)) * amplitude

A3 = 220.0

# Build three chords using frequency ratios
# Major chord: root, major third (+4 semitones), perfect fifth (+7)
# Minor chord: root, minor third (+3 semitones), perfect fifth (+7)

am = chord([semitones(A3, 0), semitones(A3, 3), semitones(A3, 7)], 1.5)  # A minor
C  = chord([semitones(A3, 3), semitones(A3, 7), semitones(A3, 10)], 1.5) # C major
G  = chord([semitones(A3, 10), semitones(A3, 14), semitones(A3, 17)], 1.5) # G major

progression = np.concatenate([am, C, G, am])
# play(progression)
# save(progression, "chords.wav")

def kick(duration=0.4):
    """Low thump — a sine wave that drops in pitch quickly."""
    t = timeline(duration)
    freq_env = np.exp(-t * 20) * 150 + 50   # pitch drops from 200 to 50 Hz
    wave = np.sin(2 * np.pi * np.cumsum(freq_env) / SR)
    env  = np.exp(-t * 10)
    return 0.8 * wave * env

def snare(duration=0.2):
    """Snappy noise burst — filtered white noise."""
    t = timeline(duration)
    noise = np.random.uniform(-1, 1, len(t))
    env   = np.exp(-t * 20)
    return 0.5 * noise * env

def hihat(duration=0.05):
    """Short high noise click."""
    t = timeline(duration)
    noise = np.random.uniform(-1, 1, len(t))
    env   = np.exp(-t * 60)
    return 0.3 * noise * env

def place(sound, position_seconds, total_length_seconds):
    """Place a sound at a position in a longer buffer."""
    buf   = np.zeros(int(SR * total_length_seconds))
    start = int(SR * position_seconds)
    end   = start + len(sound)
    if end <= len(buf):
        buf[start:end] += sound
    return buf

# One measure = 2 seconds, 8 eighth-note slots
BPM       = 120
beat      = 60 / BPM          # one beat in seconds
measure   = beat * 4           # 4 beats per measure
slot      = beat / 2           # eighth note

# Patterns: 1 = hit, 0 = rest
kick_pat   = [1, 0, 0, 0, 1, 0, 0, 0]
snare_pat  = [0, 0, 0, 1, 0, 0, 0, 1]
hihat_pat  = [0, 0, 0, 0, 0, 0, 0, 0]

buf = np.zeros(int(SR * measure))
for i, hit in enumerate(kick_pat):
    if hit: buf += place(kick(),  i * slot, measure)
for i, hit in enumerate(snare_pat):
    if hit: buf += place(snare(), i * slot, measure)
for i, hit in enumerate(hihat_pat):
    if hit: buf += place(hihat(), i * slot, measure)

buf /= np.max(np.abs(buf))

# Loop it 4 times
beat_loop = np.tile(buf, 4)
# play(beat_loop)
# save(beat_loop, "beat.wav")

def echo(wave, delay_seconds=0.3, decay=0.5, num_echoes=4):
    delay_samples = int(SR * delay_seconds)
    output = wave.copy()
    for i in range(1, num_echoes + 1):
        pad    = np.zeros(delay_samples * i)
        echo_i = np.concatenate([pad, wave * (decay ** i)])
        # match lengths
        if len(echo_i) > len(output):
            output = np.concatenate([output, np.zeros(len(echo_i) - len(output))])
        output[:len(echo_i)] += echo_i
    return output / np.max(np.abs(output)) * 0.8

dry = np.concatenate([note(440, 0.3), np.zeros(int(SR * 0.5)),
                      note(550, 0.3), np.zeros(int(SR * 0.5))])
wet = echo(dry, delay_seconds=0.2, decay=0.5)

# play(dry)
# play(wet)
# save(wet, "echo.wav")


def reverb(wave, room_size=0.3, num_reflections=80):
    output = wave.copy().astype(np.float64)
    max_delay = int(SR * room_size)
    for _ in range(num_reflections):
        delay   = np.random.randint(100, max_delay)
        decay   = np.random.uniform(0.1, 0.4)
        pad     = np.zeros(delay)
        reflect = np.concatenate([pad, wave * decay])
        if len(reflect) > len(output):
            output = np.concatenate([output, np.zeros(len(reflect) - len(output))])
        output[:len(reflect)] += reflect
    return output / np.max(np.abs(output)) * 0.8

dry  = note(440, 1.0, amplitude=0.5)
wet  = reverb(dry, room_size=0.3)
cave = reverb(dry, room_size=1.5, num_reflections=200)

# play(dry)
# play(wet)
# play(cave)
# save(cave, "reverb.wav")


def distort(wave, gain=10.0, clip=0.3):
    """Amplify then hard-clip."""
    driven = wave * gain
    return np.clip(driven, -clip, clip) * (0.8 / clip)

dry        = note(220, 1.5, amplitude=0.3, waveform='sine')
mild_dist  = distort(dry, gain=3,  clip=0.5)
heavy_dist = distort(dry, gain=20, clip=0.1)

# show(dry,        "clean",         duration=0.01)
# show(mild_dist,  "mild distortion", duration=0.01)
# show(heavy_dist, "heavy distortion", duration=0.01)

# play(dry)
# play(mild_dist)
# play(heavy_dist)

def lowpass(wave, cutoff_hz=800):
    """Apply a butterworth low-pass filter."""
    nyq = SR / 2
    b, a = butter(4, cutoff_hz / nyq, btype='low')
    return lfilter(b, a, wave)

dry      = note(440, 1.5, waveform='sawtooth')
muffled  = lowpass(dry, cutoff_hz=500)
brighter = lowpass(dry, cutoff_hz=3000)

play(dry)
play(muffled)
play(brighter)
save(muffled, "filtered.wav")