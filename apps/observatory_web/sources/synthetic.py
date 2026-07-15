"""Synthetic sources for early dashboard development."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from random import Random
from typing import Any

from .base import SpectrumFrame
from .dsp import fft


@dataclass(frozen=True)
class Tone:
    frequency_hz: int
    amplitude: float
    color: str
    label: str


class SyntheticSpectrumSource:
    """Generate a repeatable two-tone spectrum frame.

    This source behaves like a tiny software signal generator. It lets the web
    app act like an instrument before physical acquisition hardware is ready.
    """

    name = "synthetic-dual-tone"
    sample_rate_hz = 64_000
    fft_size = 4096
    max_frequency_hz = 12_000
    db_floor = -90
    waveform_view_seconds = 0.004

    tones = (
        Tone(1_000, 0.72, "#2563eb", "1 kHz reference tone"),
        Tone(10_000, 0.36, "#dc2626", "10 kHz weaker tone"),
    )

    def snapshot(self) -> SpectrumFrame:
        frame_time = time.time()
        samples = self._generate_signal(frame_time)
        spectrum = self._positive_spectrum(samples)
        peaks = [self._peak_for_tone(tone, spectrum) for tone in self.tones]
        waveform = self._waveform_points(samples)

        visible_bins = [
            {"frequency_hz": round(frequency_hz, 3), "db": round(db_value, 2)}
            for frequency_hz, db_value in spectrum
            if frequency_hz <= self.max_frequency_hz
        ]

        return {
            "source": self.name,
            "generated_at": frame_time,
            "sample_rate_hz": self.sample_rate_hz,
            "fft_size": self.fft_size,
            "bin_spacing_hz": self.bin_spacing_hz,
            "max_frequency_hz": self.max_frequency_hz,
            "db_floor": self.db_floor,
            "tones": [
                {
                    "frequency_hz": tone.frequency_hz,
                    "amplitude": tone.amplitude,
                    "label": tone.label,
                    "color": tone.color,
                }
                for tone in self.tones
            ],
            "peaks": peaks,
            "waveform": waveform,
            "spectrum": visible_bins,
        }

    @property
    def bin_spacing_hz(self) -> float:
        return self.sample_rate_hz / self.fft_size

    def _generate_signal(self, frame_time: float) -> list[complex]:
        rng = Random(int(frame_time * 10))
        samples: list[complex] = []
        slow_phase = frame_time % 1.0

        for index in range(self.fft_size):
            sample_time = index / self.sample_rate_hz
            value = 0.0
            for tone in self.tones:
                phase = 2 * math.pi * tone.frequency_hz * sample_time
                value += tone.amplitude * math.sin(phase + slow_phase)
            value += 0.018 * (rng.random() * 2 - 1)
            samples.append(complex(value, 0.0))

        return samples

    def _waveform_points(self, samples: list[complex]) -> list[dict[str, float]]:
        view_count = int(self.sample_rate_hz * self.waveform_view_seconds)
        visible = samples[:view_count]
        max_abs = max(abs(sample.real) for sample in visible) or 1.0

        return [
            {
                "time_ms": round((index / self.sample_rate_hz) * 1000, 4),
                "amplitude": round(sample.real / max_abs, 5),
            }
            for index, sample in enumerate(visible)
        ]

    def _positive_spectrum(self, samples: list[complex]) -> list[tuple[float, float]]:
        spectrum = fft(samples)
        positive_bins = spectrum[: self.fft_size // 2 + 1]
        magnitudes = [abs(value) / (self.fft_size / 2) for value in positive_bins]
        strongest = max(magnitudes) or 1.0

        points: list[tuple[float, float]] = []
        for bin_index, magnitude in enumerate(magnitudes):
            frequency_hz = bin_index * self.bin_spacing_hz
            relative = max(magnitude / strongest, 10 ** (self.db_floor / 20))
            points.append((frequency_hz, 20 * math.log10(relative)))

        return points

    def _peak_for_tone(self, tone: Tone, spectrum: list[tuple[float, float]]) -> dict[str, Any]:
        bin_index = round(tone.frequency_hz / self.bin_spacing_hz)
        frequency_hz, db_value = spectrum[bin_index]
        return {
            "label": tone.label,
            "expected_hz": tone.frequency_hz,
            "bin_frequency_hz": round(frequency_hz, 3),
            "db": round(db_value, 2),
            "color": tone.color,
        }
