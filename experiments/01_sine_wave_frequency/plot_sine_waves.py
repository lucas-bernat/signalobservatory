"""Generate a visual comparison of 1 kHz and 10 kHz sine waves.

This experiment intentionally avoids external plotting libraries. It writes a
simple SVG so the relationship between frequency, samples, and time stays
visible in the code.
"""

from math import pi, sin
from pathlib import Path


SAMPLE_RATE_HZ = 100_000
DURATION_SECONDS = 0.002
FREQUENCIES_HZ = (1_000, 10_000)

WIDTH = 1100
HEIGHT = 760
LEFT = 90
RIGHT = 40
PLOT_WIDTH = WIDTH - LEFT - RIGHT
PANEL_HEIGHT = 220
PANEL_GAP = 95
TOPS = (120, 120 + PANEL_HEIGHT + PANEL_GAP)
AMPLITUDE_SCALE = 80


def generate_times() -> list[float]:
    sample_count = int(SAMPLE_RATE_HZ * DURATION_SECONDS) + 1
    return [index / SAMPLE_RATE_HZ for index in range(sample_count)]


def sine_wave(frequency_hz: int, times: list[float]) -> list[float]:
    return [sin(2 * pi * frequency_hz * time_s) for time_s in times]


def x_for_time(time_s: float) -> float:
    return LEFT + (time_s / DURATION_SECONDS) * PLOT_WIDTH


def y_for_value(value: float, top: int) -> float:
    center_y = top + PANEL_HEIGHT / 2
    return center_y - value * AMPLITUDE_SCALE


def polyline(points: list[tuple[float, float]], color: str) -> str:
    point_text = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{point_text}" fill="none" '
        f'stroke="{color}" stroke-width="2.5" />'
    )


def circle(x: float, y: float, color: str) -> str:
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.3" fill="{color}" opacity="0.55" />'


def line(x1: float, y1: float, x2: float, y2: float, color: str, width: float = 1) -> str:
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{width}" />'
    )


def text(x: float, y: float, content: str, size: int = 18, weight: str = "400") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="#1f2937">{content}</text>'
    )


def render_panel(frequency_hz: int, times: list[float], values: list[float], top: int, color: str) -> list[str]:
    elements: list[str] = []
    bottom = top + PANEL_HEIGHT
    center_y = top + PANEL_HEIGHT / 2
    cycles = frequency_hz * DURATION_SECONDS

    elements.append(text(LEFT, top - 26, f"{frequency_hz // 1000} kHz sine wave: {cycles:g} cycles in 2 ms", 22, "700"))

    # Frame and horizontal reference lines.
    elements.append(f'<rect x="{LEFT}" y="{top}" width="{PLOT_WIDTH}" height="{PANEL_HEIGHT}" fill="#ffffff" stroke="#d1d5db" />')
    elements.append(line(LEFT, center_y, LEFT + PLOT_WIDTH, center_y, "#9ca3af", 1.2))
    elements.append(line(LEFT, y_for_value(1, top), LEFT + PLOT_WIDTH, y_for_value(1, top), "#e5e7eb"))
    elements.append(line(LEFT, y_for_value(-1, top), LEFT + PLOT_WIDTH, y_for_value(-1, top), "#e5e7eb"))

    # Vertical time grid every 0.5 ms.
    for tick_ms in (0, 0.5, 1.0, 1.5, 2.0):
        tick_s = tick_ms / 1000
        x = x_for_time(tick_s)
        elements.append(line(x, top, x, bottom, "#eef2f7"))
        elements.append(text(x - 18, bottom + 28, f"{tick_ms:g} ms", 13))

    elements.append(text(22, center_y + 5, "0", 13))
    elements.append(text(18, y_for_value(1, top) + 5, "+1", 13))
    elements.append(text(22, y_for_value(-1, top) + 5, "-1", 13))

    points = [(x_for_time(time_s), y_for_value(value, top)) for time_s, value in zip(times, values)]
    elements.append(polyline(points, color))

    # Draw sample points. These are the same sample times in both panels.
    for x, y in points:
        elements.append(circle(x, y, color))

    return elements


def render_svg() -> str:
    times = generate_times()
    waves = {frequency: sine_wave(frequency, times) for frequency in FREQUENCIES_HZ}
    colors = {1_000: "#2563eb", 10_000: "#dc2626"}

    elements: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<rect width="100%" height="100%" fill="#f8fafc" />',
        text(LEFT, 42, "Same sample rate, same time window, different frequency", 26, "700"),
        text(LEFT, 68, "Sample rate: 100,000 samples/second. Time window: 2 ms.", 15),
    ]

    for frequency, top in zip(FREQUENCIES_HZ, TOPS):
        elements.extend(render_panel(frequency, times, waves[frequency], top, colors[frequency]))

    elements.append(text(LEFT, HEIGHT - 36, "Frequency is cycles per second: 10 kHz completes 10x as many cycles as 1 kHz in the same time.", 17, "700"))
    elements.append("</svg>")
    return "\n".join(elements)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    output_dir = repo_root / "experiments" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "01_sine_wave_frequency.svg"
    output_path.write_text(render_svg(), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
