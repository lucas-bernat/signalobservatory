# Signal Observatory
## Product Requirements Document (PRD) v1.0

**Author:** Lucas Bernat  
**Status:** Draft  
**Version:** 1.0

---

# Vision

Signal Observatory is a long-term personal scientific laboratory and engineering platform.

Its purpose is **not** to build another SDR application, weather station, or dashboard.

Its purpose is to build a modular scientific observatory that allows me to observe, measure and understand physical phenomena that are normally invisible.

The project should help me explore:

- Radio waves
- Electromagnetic signals
- Satellites
- Weather
- Aircraft transmissions
- Astronomical phenomena
- Information itself

The project is strongly inspired by Claude Shannon and Information Theory.

Every module should answer scientific questions rather than simply displaying data.

---

# Philosophy

## Learn First

This project exists primarily for learning.

Every component should teach me something.

I don't just want working software.

I want to understand:

- Why it works
- How it works
- The mathematics behind it
- The engineering tradeoffs

Whenever implementing a feature, explain the concepts involved.

## Build an Instrument

Signal Observatory should feel like a scientific instrument, even if its interface is a modern web application.

Every feature should contribute to making the observatory a better scientific tool.

## Modular Design

Every subsystem should be independent.

Future modules should plug into the existing architecture without requiring major rewrites.

## Simplicity

Avoid unnecessary complexity.

Prefer readable code.

Prefer explicit code over clever code.

Build incrementally.

---

# Cloud-Ready Architecture

Signal Observatory should ultimately become a web-based scientific platform.

The Raspberry Pi will act as an **edge device**, responsible for collecting measurements from connected hardware such as SDRs, sensors, cameras and future scientific instruments.

The primary user interface should be a web application accessible from any device.

The architecture should separate:

- Edge Device (hardware acquisition)
- Backend (processing, APIs and storage)
- Frontend (scientific dashboard)

Initially all services may run on the Raspberry Pi.

As the project grows, components should be easy to migrate to cloud infrastructure.

The long-term vision is to support multiple observatories distributed around the world, all connected to a common backend.

---

# High-Level Architecture

```
Browser
    │
Frontend (React/Next.js)
    │
REST API
    │
Backend (FastAPI)
    │
Database
    │
──────────── Internet ────────────
    │
Edge Device (Raspberry Pi)
    │
RTL-SDR • Sensors • Cameras • GPS
```

---

# Hardware

## Initial

- Raspberry Pi 5
- RTL-SDR Blog V4
- Standard antenna
- Mac for development
- SSH

## Future

- Better antennas
- Weather station
- GPS
- All-sky camera
- Lightning detector
- Air quality sensors
- Radio astronomy antenna
- Oscilloscope

---

# Development Roadmap

## Phase 1 — Spectrum Analyzer

Build a real-time spectrum analyzer.

Features:

- RTL-SDR integration
- IQ sample acquisition
- FFT
- Spectrum visualization
- Waterfall
- Peak detection
- SQLite logging

Learn:

- Sampling
- IQ
- FFT
- Frequency
- Noise
- SNR

---

## Phase 2 — Signal Intelligence

- Automatic signal detection
- Signal classification
- Occupancy statistics
- Daily reports
- Noise floor estimation

---

## Phase 3 — ADS-B

Receive aircraft transmissions directly.

Learn packet decoding and radio protocols.

---

## Phase 4 — Weather Satellites

Receive and decode NOAA weather satellite imagery.

---

## Phase 5 — Meteorology

Integrate sensors for:

- Temperature
- Pressure
- Humidity
- Wind
- Rain
- Air quality

---

## Phase 6 — Astronomy

Track:

- Sun
- Moon
- ISS
- Planets
- Satellites

Later add amateur radio astronomy.

---

## Phase 7 — Antenna Laboratory

Experiment with antenna gain, polarization, orientation and noise.

---

## Phase 8 — Information Theory

Inspired by Claude Shannon.

Implement visualizations for:

- Entropy
- Bandwidth
- SNR
- Channel capacity

---

## Phase 9 — AI Scientist

Use AI to:

- Detect anomalies
- Discover patterns
- Summarize observations
- Suggest experiments

---

# Suggested Repository Structure

```text
signal-observatory/

backend/
    acquisition/
    processing/
    storage/
    api/

frontend/

experiments/

docs/

data/

scripts/

tests/

SIGNAL_OBSERVATORY_PRD.md
```

---

# Non-Goals

The project is **not** intended to:

- Replace professional SDR software.
- Optimize for maximum performance before understanding the concepts.
- Support every SDR device from day one.
- Introduce machine learning before building a solid DSP foundation.

---

# Working Style

Act as my software architect, DSP engineer, educator and mentor.

Do not simply generate code.

Explain every important concept.

Discuss architectural tradeoffs before implementation.

Optimize for:

- Scientific understanding
- Clean architecture
- Maintainability
- Incremental progress

The objective is not only to build software.

The objective is to build knowledge.
