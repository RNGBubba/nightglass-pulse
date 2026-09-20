import math
import random
import struct
import wave
from pathlib import Path

SR = 44100
BPM = 120
BEAT = 60.0 / BPM
BARS = 10
DURATION = BARS * 4 * BEAT
N = int(SR * DURATION)
OUT = Path(__file__).parent / "nightglass-pulse.wav"
random.seed(1947)

# A compact, original motif in D dorian. The motif, rhythm, and synth voices
# were written for this loop rather than transcribed from an existing work.
chords = [
    ["D3", "F3", "A3", "C4", "E4"],
    ["Bb2", "D3", "F3", "A3", "C4"],
    ["G2", "Bb2", "D3", "F3", "A3"],
    ["A2", "D3", "E3", "G3", "B3"],
    ["D3", "F3", "A3", "C4", "E4"],
    ["Bb2", "D3", "F3", "A3", "C4"],
    ["G2", "Bb2", "D3", "F3", "A3"],
    ["A2", "D3", "E3", "G3", "B3"],
    ["D3", "F3", "A3", "C4", "E4"],
    ["A2", "D3", "E3", "G3", "B3"],
]
semitone = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
            "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
            "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

def hz(note):
    name = note[:-1]
    octave = int(note[-1])
    midi = (octave + 1) * 12 + semitone[name]
    return 440.0 * 2 ** ((midi - 69) / 12)

def add(buf, start, length, freq, amp, kind="sine", pan=0.0):
    left = (1.0 - pan) * 0.5
    right = (1.0 + pan) * 0.5
    stop = min(N, start + length)
    for i in range(start, stop):
        x = (i - start) / SR
        t = i - start
        attack = min(1.0, t / (0.012 * SR))
        release = min(1.0, max(0.0, (stop - i) / (0.08 * SR)))
        env = attack * release
        if kind == "pad":
            s = (math.sin(2 * math.pi * freq * x) + 0.35 * math.sin(2 * math.pi * freq * 2.01 * x)) * 0.5
        elif kind == "bass":
            s = math.sin(2 * math.pi * freq * x) + 0.18 * math.sin(2 * math.pi * freq * 2 * x)
            env *= min(1.0, x / 0.04)
        elif kind == "pluck":
            env *= math.exp(-4.0 * x)
            s = math.sin(2 * math.pi * freq * x) + 0.22 * math.sin(2 * math.pi * freq * 2.0 * x)
        else:
            s = math.sin(2 * math.pi * freq * x)
        s *= amp * env
        buf[2 * i] += s * left
        buf[2 * i + 1] += s * right

def noise_hit(buf, start, amp, decay, pan=0.0):
    left = (1.0 - pan) * 0.5
    right = (1.0 + pan) * 0.5
    length = min(N - start, int(0.16 * SR))
    for j in range(length):
        x = j / SR
        s = random.uniform(-1.0, 1.0) * math.exp(-decay * x) * amp
        idx = 2 * (start + j)
        buf[idx] += s * left
        buf[idx + 1] += s * right

buf = [0.0] * (2 * N)
bar_samples = int(4 * BEAT * SR)

# Warm, sustained chord bed.
for bar, chord in enumerate(chords):
    start = bar * bar_samples
    for note in chord:
        add(buf, start, bar_samples + int(0.05 * SR), hz(note), 0.055, "pad", pan=-0.18 if bar % 2 else 0.18)

# Rounded bass: roots on beats 1 and 3, with a pickup before each new bar.
for bar, chord in enumerate(chords):
    root = chord[0]
    for beat in (0, 2):
        start = int((bar * 4 + beat) * BEAT * SR)
        add(buf, start, int(1.7 * BEAT * SR), hz(root) / 2, 0.22, "bass", pan=0.0)
    if bar > 0:
        start = int((bar * 4 - 0.25) * BEAT * SR)
        add(buf, start, int(0.3 * BEAT * SR), hz(root) / 2, 0.11, "bass", pan=0.0)

# Dry, syncopated original pluck motif. The second half answers the first.
motif = [
    (0.0, "D5"), (0.75, "F5"), (1.5, "A5"), (2.25, "C6"),
    (3.0, "A5"), (3.5, "F5"),
    (4.0, "D5"), (4.5, "E5"), (5.25, "G5"), (6.0, "A5"),
    (6.75, "G5"), (7.5, "E5"),
]
for bar in range(BARS):
    shift = 0.0 if bar % 2 == 0 else 0.12
    for beat, note in motif:
        start = int((bar * 4 + beat + shift) * BEAT * SR)
        add(buf, start, int(0.28 * BEAT * SR), hz(note), 0.12, "pluck", pan=-0.32 if (bar + int(beat)) % 2 else 0.32)

# Four-on-the-floor kick, backbeat, and low-level hats.
for beat_index in range(BARS * 4):
    start = int(beat_index * BEAT * SR)
    # synthesized kick with a descending pitch sweep
    length = min(N - start, int(0.22 * SR))
    for j in range(length):
        x = j / SR
        s = math.sin(2 * math.pi * (105 - 65 * min(1.0, x / 0.18)) * x)
        s *= 0.36 * math.exp(-15 * x)
        idx = 2 * (start + j)
        buf[idx] += s * 0.5
        buf[idx + 1] += s * 0.5
    if beat_index % 4 in (1, 3):
        noise_hit(buf, start, 0.16, 28, pan=0.05)
    for eighth in (0.5, 1.5, 2.5, 3.5):
        hstart = int((beat_index + eighth) * BEAT * SR)
        noise_hit(buf, hstart, 0.035, 55, pan=-0.15 if beat_index % 2 else 0.15)

# Gentle saturation, peak normalization, and a short loop-safe tail crossfade.
peak = max(1e-9, max(abs(x) for x in buf))
scale = 0.86 / peak
for i, x in enumerate(buf):
    buf[i] = math.tanh(x * scale * 1.15) / 1.15

fade = int(0.08 * SR)
for j in range(fade):
    t = j / fade
    for ch in (0, 1):
        tail = 2 * (N - fade + j) + ch
        head = 2 * j + ch
        buf[tail] = buf[tail] * (1.0 - t) + buf[head] * t

with wave.open(str(OUT), "wb") as f:
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(SR)
    frames = bytearray()
    for x in buf:
        frames.extend(struct.pack("<h", max(-32768, min(32767, int(x * 32767)))))
    f.writeframes(frames)

print(f"wrote {OUT} ({N / SR:.2f}s stereo {SR}Hz)")
