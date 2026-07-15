"""Small DSP helpers used by observatory sources."""

from __future__ import annotations

import math
from cmath import exp


def fft(samples: list[complex]) -> list[complex]:
    """Return a radix-2 Cooley-Tukey FFT for a power-of-two sample list.

    This is intentionally simple and dependency-free for early learning. We can
    replace it with NumPy later when performance becomes more important than
    being able to read the transform directly.
    """

    sample_count = len(samples)
    if sample_count == 1:
        return samples

    even_bins = fft(samples[0::2])
    odd_bins = fft(samples[1::2])
    output = [0j] * sample_count
    half_count = sample_count // 2

    for index in range(half_count):
        twiddle = exp(-2j * math.pi * index / sample_count) * odd_bins[index]
        output[index] = even_bins[index] + twiddle
        output[index + half_count] = even_bins[index] - twiddle

    return output
