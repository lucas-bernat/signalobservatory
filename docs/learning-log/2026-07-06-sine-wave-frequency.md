# 2026-07-06: Sine Wave Frequency

## Question

What changes visually when two sine waves have different frequencies but the same sample rate and the same time window?

## Setup

- Hardware: Mac development machine
- Software: Python 3
- Location: local repo
- Antenna: none
- Frequency or band: synthetic 1 kHz and 10 kHz tones

## Commands Or Procedure

```bash
python3 experiments/01_sine_wave_frequency/plot_sine_waves.py
```

## Observations

- Both waves are plotted over the same 2 millisecond window.
- The 1 kHz wave completes 2 cycles.
- The 10 kHz wave completes 20 cycles.
- The 10 kHz wave looks more tightly packed because it changes faster.
- The sample rate is the same for both plots: 100,000 samples per second.

## Explanation

Frequency means cycles per second.

```text
1 kHz  = 1,000 cycles/second
10 kHz = 10,000 cycles/second
```

The observation window is 2 milliseconds:

```text
2 ms = 0.002 seconds
```

So the number of cycles in the window is:

```text
cycles = frequency * time

1 kHz:  1,000 * 0.002  = 2 cycles
10 kHz: 10,000 * 0.002 = 20 cycles
```

## Diagram Or Mental Model

```text
same 2 ms time window

1 kHz:   / \       / \
        /   \     /   \
-------/-----\---/-----\-----

10 kHz: /\/\/\/\/\/\/\/\/\/\
```

The time window did not change. The sample rate did not change. Only the frequency changed, so the faster wave completes more cycles inside the same window.

Generated plot:

```text
experiments/output/01_sine_wave_frequency.svg
```

## Mistakes Or Confusions

- It is easy to think "higher frequency" means "bigger" or "louder." It does not.
- Frequency is about how quickly the wave repeats, not how tall the wave is.

## Result

A 10 kHz sine wave completes ten times as many cycles as a 1 kHz sine wave over the same duration.

## Next Question

What happens if the sample rate is too low to represent the faster wave correctly?
