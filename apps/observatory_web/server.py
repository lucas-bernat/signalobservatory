"""Signal Observatory web dashboard.

This first app uses a synthetic signal source so the web/API/data flow can be
learned before the RTL-SDR hardware arrives. It intentionally depends only on
the Python standard library so it can run on a fresh Raspberry Pi.
"""

from __future__ import annotations

import argparse
import json
import math
import mimetypes
import os
import platform
import socket
import time
from cmath import exp
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from random import Random
from typing import Any
from urllib.parse import urlparse


APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"


@dataclass(frozen=True)
class Tone:
    frequency_hz: int
    amplitude: float
    color: str
    label: str


class SyntheticSpectrumSource:
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

    def snapshot(self) -> dict[str, Any]:
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


def fft(samples: list[complex]) -> list[complex]:
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


class ObservatoryRequestHandler(BaseHTTPRequestHandler):
    source = SyntheticSpectrumSource()
    server_version = "SignalObservatoryWeb/0.1"

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path == "/":
            self._send_static_file(STATIC_DIR / "index.html")
            return

        if path == "/api/status":
            self._send_json(
                {
                    "name": "Signal Observatory",
                    "hostname": socket.gethostname(),
                    "platform": platform.platform(),
                    "python_version": platform.python_version(),
                    "server_time": time.time(),
                    "source": self.source.name,
                    "working_directory": os.getcwd(),
                }
            )
            return

        if path == "/api/spectrum":
            self._send_json(self.source.snapshot())
            return

        if path.startswith("/static/"):
            requested = path.removeprefix("/static/")
            self._send_static_file(STATIC_DIR / requested)
            return

        self._send_json({"error": "not found", "path": path}, HTTPStatus.NOT_FOUND)

    def log_message(self, format_string: str, *args: Any) -> None:
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} {format_string % args}")

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_static_file(self, path: Path) -> None:
        resolved = path.resolve()
        if not resolved.is_file() or STATIC_DIR.resolve() not in resolved.parents:
            self._send_json({"error": "static file not found"}, HTTPStatus.NOT_FOUND)
            return

        body = resolved.read_bytes()
        content_type, _ = mimetypes.guess_type(resolved.name)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Signal Observatory web dashboard.")
    parser.add_argument("--host", default="127.0.0.1", help="Host/interface to bind.")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ObservatoryRequestHandler)
    print(f"Signal Observatory web app listening on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Signal Observatory web app.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
