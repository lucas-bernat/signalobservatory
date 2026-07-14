"""Generate a time-domain signal and its FFT spectrum.

This experiment intentionally uses only the Python standard library. The goal
is to make the FFT idea runnable on a freshly configured Raspberry Pi before
any SDR hardware or scientific Python packages are installed.
"""

from __future__ import annotations

from cmath import exp
from math import log10, pi, sin
from pathlib import Path
from random import Random


SAMPLE_RATE_HZ = 64_000
FFT_SIZE = 4096
TONE_A_HZ = 1_000
TONE_B_HZ = 10_000
TONE_A_AMPLITUDE = 0.72
TONE_B_AMPLITUDE = 0.36
NOISE_AMPLITUDE = 0.025
TIME_VIEW_SECONDS = 0.004
MAX_PLOT_FREQUENCY_HZ = 12_000
DB_FLOOR = -80

WIDTH = 1180
HEIGHT = 860
LEFT = 96
RIGHT = 48
PLOT_WIDTH = WIDTH - LEFT - RIGHT
TIME_TOP = 120
TIME_HEIGHT = 250
SPECTRUM_TOP = 500
SPECTRUM_HEIGHT = 270


def generate_signal() -> list[complex]:
    rng = Random(20260714)
    samples: list[complex] = []

    for index in range(FFT_SIZE):
        time_s = index / SAMPLE_RATE_HZ
        tone_a = TONE_A_AMPLITUDE * sin(2 * pi * TONE_A_HZ * time_s)
        tone_b = TONE_B_AMPLITUDE * sin(2 * pi * TONE_B_HZ * time_s)
        noise = NOISE_AMPLITUDE * (rng.random() * 2 - 1)
        samples.append(complex(tone_a + tone_b + noise, 0.0))

    return samples


def fft(samples: list[complex]) -> list[complex]:
    """A small radix-2 Cooley-Tukey FFT.

    The input length must be a power of two. We use a clear recursive version
    here because the experiment is about seeing the idea, not optimizing speed.
    """

    sample_count = len(samples)
    if sample_count == 1:
        return samples

    even_bins = fft(samples[0::2])
    odd_bins = fft(samples[1::2])
    output = [0j] * sample_count
    half_count = sample_count // 2

    for index in range(half_count):
        twiddle = exp(-2j * pi * index / sample_count) * odd_bins[index]
        output[index] = even_bins[index] + twiddle
        output[index + half_count] = even_bins[index] - twiddle

    return output


def bin_spacing_hz() -> float:
    return SAMPLE_RATE_HZ / FFT_SIZE


def positive_spectrum(samples: list[complex]) -> list[tuple[float, float]]:
    spectrum = fft(samples)
    positive_bins = spectrum[: FFT_SIZE // 2 + 1]
    magnitudes = [abs(value) / (FFT_SIZE / 2) for value in positive_bins]
    strongest = max(magnitudes)

    points: list[tuple[float, float]] = []
    for bin_index, magnitude in enumerate(magnitudes):
        frequency_hz = bin_index * bin_spacing_hz()
        relative = max(magnitude / strongest, 10 ** (DB_FLOOR / 20))
        db_relative = 20 * log10(relative)
        points.append((frequency_hz, db_relative))

    return points


def nearest_bin(frequency_hz: int) -> int:
    return round(frequency_hz / bin_spacing_hz())


def line(x1: float, y1: float, x2: float, y2: float, color: str, width: float = 1.0) -> str:
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{width}" />'
    )


def text(x: float, y: float, content: str, size: int = 16, weight: str = "400", color: str = "#1f2937") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{content}</text>'
    )


def polyline(points: list[tuple[float, float]], color: str, width: float = 2.0) -> str:
    point_text = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{point_text}" fill="none" '
        f'stroke="{color}" stroke-width="{width}" stroke-linejoin="round" />'
    )


def x_for_time(time_s: float) -> float:
    return LEFT + (time_s / TIME_VIEW_SECONDS) * PLOT_WIDTH


def y_for_sample(value: float, max_abs: float) -> float:
    center_y = TIME_TOP + TIME_HEIGHT / 2
    return center_y - (value / max_abs) * (TIME_HEIGHT * 0.42)


def x_for_frequency(frequency_hz: float) -> float:
    return LEFT + (frequency_hz / MAX_PLOT_FREQUENCY_HZ) * PLOT_WIDTH


def y_for_db(db_relative: float) -> float:
    clipped = max(DB_FLOOR, min(0, db_relative))
    normalized = (clipped - DB_FLOOR) / abs(DB_FLOOR)
    return SPECTRUM_TOP + SPECTRUM_HEIGHT - normalized * SPECTRUM_HEIGHT


def render_time_panel(samples: list[complex]) -> list[str]:
    view_count = int(SAMPLE_RATE_HZ * TIME_VIEW_SECONDS)
    visible_samples = samples[:view_count]
    max_abs = max(abs(sample.real) for sample in visible_samples)
    bottom = TIME_TOP + TIME_HEIGHT
    center_y = TIME_TOP + TIME_HEIGHT / 2

    elements: list[str] = [
        text(LEFT, TIME_TOP - 42, "Time domain: mixed synthetic signal", 22, "700"),
        text(LEFT, TIME_TOP - 18, "The raw samples contain both tones at once, plus a tiny noise floor.", 15, "400", "#667085"),
        f'<rect x="{LEFT}" y="{TIME_TOP}" width="{PLOT_WIDTH}" height="{TIME_HEIGHT}" fill="#ffffff" stroke="#d1d5db" />',
        line(LEFT, center_y, LEFT + PLOT_WIDTH, center_y, "#9ca3af", 1.2),
    ]

    for tick_ms in range(0, 5):
        time_s = tick_ms / 1000
        x = x_for_time(time_s)
        elements.append(line(x, TIME_TOP, x, bottom, "#eef2f7"))
        elements.append(text(x - 16, bottom + 26, f"{tick_ms} ms", 13))

    points = [
        (x_for_time(index / SAMPLE_RATE_HZ), y_for_sample(sample.real, max_abs))
        for index, sample in enumerate(visible_samples)
    ]
    elements.append(polyline(points, "#2563eb", 2.2))
    elements.append(text(20, center_y + 5, "0", 13, "400", "#667085"))
    return elements


def render_spectrum_panel(spectrum_points: list[tuple[float, float]]) -> list[str]:
    bottom = SPECTRUM_TOP + SPECTRUM_HEIGHT
    visible_points = [
        (frequency_hz, db_relative)
        for frequency_hz, db_relative in spectrum_points
        if frequency_hz <= MAX_PLOT_FREQUENCY_HZ
    ]

    elements: list[str] = [
        text(LEFT, SPECTRUM_TOP - 42, "Frequency domain: FFT magnitude spectrum", 22, "700"),
        text(LEFT, SPECTRUM_TOP - 18, "The same samples become frequency bins. Strong tones become peaks.", 15, "400", "#667085"),
        f'<rect x="{LEFT}" y="{SPECTRUM_TOP}" width="{PLOT_WIDTH}" height="{SPECTRUM_HEIGHT}" fill="#ffffff" stroke="#d1d5db" />',
    ]

    for db in (0, -20, -40, -60, -80):
        y = y_for_db(db)
        elements.append(line(LEFT, y, LEFT + PLOT_WIDTH, y, "#e5e7eb"))
        elements.append(text(34, y + 5, f"{db} dB", 13, "400", "#667085"))

    for frequency_hz in range(0, MAX_PLOT_FREQUENCY_HZ + 1, 2_000):
        x = x_for_frequency(frequency_hz)
        elements.append(line(x, SPECTRUM_TOP, x, bottom, "#eef2f7"))
        elements.append(text(x - 22, bottom + 26, f"{frequency_hz // 1000} kHz", 13))

    for frequency_hz, db_relative in visible_points:
        x = x_for_frequency(frequency_hz)
        y = y_for_db(db_relative)
        if db_relative > -75:
            elements.append(line(x, bottom, x, y, "#0f766e", 1.0))

    for expected_hz, color in ((TONE_A_HZ, "#2563eb"), (TONE_B_HZ, "#dc2626")):
        bin_index = nearest_bin(expected_hz)
        bin_frequency = bin_index * bin_spacing_hz()
        bin_db = spectrum_points[bin_index][1]
        x = x_for_frequency(bin_frequency)
        y = y_for_db(bin_db)
        elements.append(line(x, SPECTRUM_TOP, x, bottom, color, 2.0))
        elements.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{color}" />')
        elements.append(text(x + 10, max(SPECTRUM_TOP + 22, y - 10), f"{expected_hz // 1000} kHz peak", 15, "700", color))

    elements.append(text(LEFT, HEIGHT - 42, f"FFT size: {FFT_SIZE} samples. Sample rate: {SAMPLE_RATE_HZ:,} Hz. Bin spacing: {bin_spacing_hz():.3f} Hz.", 16, "700"))
    return elements


def render_svg(samples: list[complex], spectrum_points: list[tuple[float, float]]) -> str:
    elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#f8fafc" />',
        text(LEFT, 44, "Synthetic signal: time view and FFT spectrum", 28, "700"),
        text(LEFT, 74, "A 1 kHz tone and a 10 kHz tone are hidden together in one sampled waveform.", 16, "400", "#667085"),
    ]
    elements.extend(render_time_panel(samples))
    elements.extend(render_spectrum_panel(spectrum_points))
    elements.append("</svg>")
    return "\n".join(elements)


def main() -> None:
    samples = generate_signal()
    spectrum_points = positive_spectrum(samples)

    repo_root = Path(__file__).resolve().parents[2]
    output_dir = repo_root / "experiments" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "03_fft_spectrum.svg"
    output_path.write_text(render_svg(samples, spectrum_points), encoding="utf-8")

    print(output_path)
    print(f"bin spacing: {bin_spacing_hz():.3f} Hz")
    for frequency_hz in (TONE_A_HZ, TONE_B_HZ):
        bin_index = nearest_bin(frequency_hz)
        bin_frequency = bin_index * bin_spacing_hz()
        bin_db = spectrum_points[bin_index][1]
        print(f"peak near {frequency_hz:>5} Hz -> bin {bin_frequency:8.3f} Hz at {bin_db:5.1f} dB")


if __name__ == "__main__":
    main()
