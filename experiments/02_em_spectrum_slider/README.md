# Experiment 02: Electromagnetic Spectrum Slider

## Question

How does frequency change across the electromagnetic spectrum, and which parts can an RTL-SDR directly observe?

## Concept

The electromagnetic spectrum spans many orders of magnitude. A normal linear slider would be useless because radio, infrared, visible light, X-rays, and gamma rays are separated by huge frequency ratios.

This experiment uses a logarithmic slider:

```text
slider position -> log10(frequency) -> frequency in Hz
```

## Run

Open this file in a browser:

```text
experiments/02_em_spectrum_slider/index.html
```

Or from the repository root:

```bash
open experiments/02_em_spectrum_slider/index.html
```

## What To Notice

- The marker moves across radio, microwave, infrared, visible, ultraviolet, X-ray, and gamma regions.
- Wavelength shrinks as frequency increases.
- The waveform visualization becomes denser as frequency increases.
- The RTL-SDR range is only a small part of the lower-frequency end of the electromagnetic spectrum.

## Important Note

The waveform plot is a scaled visual model. It shows the idea that higher frequency means more cycles in the same reference window, but it does not draw actual real-time gamma-ray oscillations.

## Why This Matters For SDR

SDR work lives in the radio-frequency part of the electromagnetic spectrum. The same physics connects radio waves to visible light and X-rays, but different sensors are needed for different regions.
