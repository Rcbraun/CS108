import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

SR = 44100
BPM = 85
BEAT = 60 / BPM          # one quarter note in seconds
SWING = 0.62             # >0.5 pushes the "and" beats late (lo-fi swing feel)

# ── Utilities ────────────────────────────────────────────────────────────────

def semitones(freq, n):
    return freq * (2 ** (n / 12))

def tone(freq, dur, amp=0.3, wave="sine"):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    if wave == "sine":
        s = np.sin(2 * np.pi * freq * t)
    elif wave == "saw":
        s = 2 * (t * freq % 1) - 1
    elif wave == "square":
        s = np.sign(np.sin(2 * np.pi * freq * t))
    # Soft envelope (attack / release)
    env = np.ones_like(t)
    a = int(0.01 * SR); r = int(0.15 * SR)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] = np.linspace(1, 0, r)
    return (s * env * amp).astype(np.float32)

def chord(freqs, dur, amp=0.18):
    return sum(tone(f, dur, amp) for f in freqs)

def silence(dur):
    return np.zeros(int(SR * dur), dtype=np.float32)

# ── Drums (synthesized) ───────────────────────────────────────────────────────

def kick(dur=0.35):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    freq = 120 * np.exp(-20 * t)          # pitch drop
    s = np.sin(2 * np.pi * freq * t)
    env = np.exp(-8 * t)
    return (s * env * 0.9).astype(np.float32)

def snare(dur=0.18):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    noise = np.random.randn(len(t))
    tone_s = np.sin(2 * np.pi * 180 * t)
    env = np.exp(-25 * t)
    return ((noise * 0.6 + tone_s * 0.4) * env * 0.55).astype(np.float32)

def hihat(dur=0.05, amp=0.12):
    t = np.linspace(0, dur, int(SR * dur), endpoint=False)
    noise = np.random.randn(len(t))
    env = np.exp(-60 * t)
    return (noise * env * amp).astype(np.float32)

# ── Pattern builder ───────────────────────────────────────────────────────────

def place(buf, clip, start_sec):
    i = int(start_sec * SR)
    end = min(i + len(clip), len(buf))
    buf[i:end] += clip[:end - i]

def make_bar(beats=4):
    """One bar of boom-bap with swing 8th notes."""
    bar_len = int(BEAT * beats * SR)
    buf = np.zeros(bar_len, dtype=np.float32)

    # Kick on 1 and 3
    for b in [0, 2]:
        place(buf, kick(), b * BEAT)

    # Snare on 2 and 4
    for b in [1, 3]:
        place(buf, snare(), b * BEAT)

    # Swung 8th-note hi-hats
    straight = BEAT / 2
    swung    = BEAT * SWING
    offbeat  = BEAT * (1 - SWING)
    for b in range(beats):
        place(buf, hihat(),       b * BEAT)                   # on the beat
        place(buf, hihat(amp=0.07), b * BEAT + swung)         # swung "and"

    # Ghost snare (quiet, add texture)
    place(buf, snare() * 0.2, 0.75 * BEAT)
    place(buf, snare() * 0.15, 2.5  * BEAT)

    return buf

# ── Chords & Bass ─────────────────────────────────────────────────────────────

A3 = 220.0

def make_chords(dur=BEAT * 4):
    am = chord([semitones(A3, 0), semitones(A3, 3), semitones(A3, 7)], dur)
    C  = chord([semitones(A3, 3), semitones(A3, 7), semitones(A3, 10)], dur)
    G  = chord([semitones(A3, 10), semitones(A3, 14), semitones(A3, 17)], dur)
    return np.concatenate([am, C, G, am])  # 4 bars

def make_bass():
    """Root notes an octave below, on beat 1 of each chord bar."""
    roots = [A3 / 2, semitones(A3, 3) / 2, semitones(A3, 10) / 2, A3 / 2]
    bars = []
    for root in roots:
        bar = silence(BEAT * 4)
        note = tone(root, BEAT * 0.9, amp=0.45, wave="sine")
        place(bar, note, 0)
        # Quick walk-up on beat 4
        walk = tone(semitones(root, 2), BEAT * 0.4, amp=0.3, wave="sine")
        place(bar, walk, BEAT * 3)
        bars.append(bar)
    return np.concatenate(bars)

def make_melody():
    """Simple pentatonic hook over the 4-bar loop."""
    # A minor pentatonic intervals (in semitones)
    penta = [0, 3, 5, 7, 10]

    # use indices into penta (NOT semitone values)
    pattern = [0, 2, 3, 2, 4, 3, 2, 0]

    notes = []
    for i, deg in enumerate(pattern):
        freq = semitones(A3 * 2, penta[deg])
        dur  = BEAT * 0.9 if i % 2 == 0 else BEAT * 0.45

        notes.append(tone(freq, dur, amp=0.12, wave="sine"))
        notes.append(silence(BEAT * 0.1))

    melody = np.concatenate(notes)

    full = silence(BEAT * 16)
    place(full, melody, 0)
    return full

# ── Assemble ──────────────────────────────────────────────────────────────────

BARS = 4
drums   = np.concatenate([make_bar() for _ in range(BARS)])
chords  = make_chords()
bass    = make_bass()
melody  = make_melody()

# Trim to shortest (floating-point length differences)
n = min(len(drums), len(chords), len(bass), len(melody))
mix = drums[:n] + chords[:n] + bass[:n] + melody[:n]

# Soft limiter
mix = np.tanh(mix * 1.2) * 0.85

print("Playing… (Ctrl+C to stop)")
sd.play(mix, SR)
sd.wait()