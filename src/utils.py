"""Shared audio helpers used by the generator and detector."""

import os

import librosa
import numpy as np
import soundfile as sf

SAMPLE_RATE = 16000


def ensure_dir(path):
    """Create a directory (and parents) if it doesn't exist yet."""
    os.makedirs(path, exist_ok=True)
    return path


def load_audio(path, sr=SAMPLE_RATE):
    """Load an audio file as a mono waveform resampled to `sr`."""
    audio, _ = librosa.load(path, sr=sr, mono=True)
    return audio


def save_audio(path, audio, sr=SAMPLE_RATE):
    """Write a waveform to disk, creating the parent directory if needed."""
    ensure_dir(os.path.dirname(path) or ".")
    sf.write(path, audio, sr)
    return path


def cosine_similarity(vec_a, vec_b):
    """Cosine similarity between two vectors, in [-1, 1]."""
    a = np.asarray(vec_a, dtype=np.float64)
    b = np.asarray(vec_b, dtype=np.float64)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)
