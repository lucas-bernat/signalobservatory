# Experiment 01: Sine Wave Frequency

## Question

What changes visually when two sine waves have different frequencies but the same sample rate and the same time window?

## Concept

Frequency means cycles per second.

If we observe the same 2 millisecond time window:

- a 1 kHz sine wave completes 2 cycles
- a 10 kHz sine wave completes 20 cycles

That is why higher frequency waves look more tightly packed in time.

## Visual Model

```text
same time window

1 kHz:   / \       / \
        /   \     /   \
-------/-----\---/-----\-----

10 kHz: /\/\/\/\/\/\/\/\/\/\
```

## Run

From the repository root:

```bash
python3 experiments/01_sine_wave_frequency/plot_sine_waves.py
```

The script writes:

```text
experiments/output/01_sine_wave_frequency.svg
```

## Settings

```text
sample rate: 100,000 samples/second
duration:    2 milliseconds
frequency 1: 1,000 Hz
frequency 2: 10,000 Hz
```

## What To Notice

- The two waves use the same time axis.
- The two waves are sampled at the same rate.
- The 10 kHz wave completes ten times as many cycles as the 1 kHz wave.
- The samples are closer together along the waveform because the waveform itself changes faster.

## Why This Matters For SDR

The SDR also gives us samples over time. Before we can understand I/Q samples and FFTs, we need to be comfortable seeing frequency as repeated cycles inside a time window.
