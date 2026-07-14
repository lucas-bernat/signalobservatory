# 2026-07-06: Electromagnetic Spectrum Slider

## Question

Can an interactive slider make frequency, wavelength, and electromagnetic spectrum regions easier to understand?

## Setup

- Hardware: Mac development machine
- Software: browser, HTML, CSS, JavaScript
- Location: local repo
- Antenna: none
- Frequency or band: synthetic electromagnetic spectrum model

## Commands Or Procedure

Open:

```bash
open experiments/02_em_spectrum_slider/index.html
```

## Observations

- The electromagnetic spectrum spans too many orders of magnitude for a normal linear scale.
- A logarithmic scale makes radio, microwave, infrared, visible, ultraviolet, X-ray, and gamma regions visible in one interface.
- Wavelength decreases as frequency increases.
- The scaled waveform becomes visually denser at higher frequencies.
- The RTL-SDR range is a small slice near the low-frequency end of the full electromagnetic spectrum.

## Explanation

Frequency and wavelength are linked by the speed of light:

```text
wavelength = speed_of_light / frequency
```

As frequency increases, wavelength shrinks.

Because the spectrum spans many powers of ten, the slider uses:

```text
slider position = log10(frequency)
```

That makes each equal slider step represent a multiplication in frequency rather than a fixed number of hertz.

## Diagram Or Mental Model

```text
low frequency                                            high frequency
long wavelength                                         short wavelength

radio -> microwave -> infrared -> visible -> UV -> X-ray -> gamma
  ^
  |
RTL-SDR observes a small lower-frequency slice directly
```

## Mistakes Or Confusions

- It is easy to think the RTL-SDR can observe the whole electromagnetic spectrum because all these waves are "electromagnetic."
- The physics is connected, but the sensor is different for different regions.
- The waveform drawing is scaled for learning. It does not draw actual gamma-ray oscillations in real time.

## Result

The interactive slider gives a visual bridge between SDR radio work and the larger electromagnetic spectrum.

## Next Question

How does a logarithmic frequency scale compare to a linear frequency scale, and why do spectrum analyzers often use log units like dB?
