# Signal Observatory
## Product Requirements Document (PRD) v1.1

**Author:** Lucas Bernat  
**Status:** Draft  
**Version:** 1.1

---

# Vision

Signal Observatory is a long-term personal scientific laboratory and engineering platform.

The current long-term direction is to evolve Signal Observatory into **The Invisible Observatory**: a modular platform for observing physical phenomena humans cannot directly perceive.

Its purpose is **not** to build another SDR application, weather station, or dashboard.

Its purpose is to build a modular scientific observatory that allows me to observe, measure and understand physical phenomena that are normally invisible.

The first concrete module is radio-frequency observation with Raspberry Pi and RTL-SDR hardware.

The broader platform should eventually help me explore:

- Radio waves
- Electromagnetic signals
- Satellites
- Weather
- Aircraft transmissions
- Astronomical phenomena
- Visible, infrared, near-infrared, thermal, solar and ultraviolet phenomena
- Cross-sensor correlations across time
- Information itself

The project is strongly inspired by Claude Shannon and Information Theory.

Every module should answer scientific questions rather than simply displaying data.

## Product Direction

The repository remains named Signal Observatory because radio is the first learning path and first hardware module.

The product concept should be designed as:

```text
Signal Observatory = first module and learning path
The Invisible Observatory = broader multi-sensor platform direction
```

Radio should not become the entire architecture. It should become one module inside a generic observatory system.

The system should eventually organize measurements around:

- Observatory
- Device
- Sensor
- Capture session
- Measurement
- Derived metric
- Observation
- Experiment

The long-term scientific interface should act like a time machine: choose a moment, then inspect what all sensors observed near that time.

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

Radio-specific behavior should live inside a radio module rather than defining the platform's core data model.

The shared platform should own observatories, devices, sensors, measurements, sessions, storage, calibration, timestamps, geolocation, timeline queries, and observations.

## Simplicity

Avoid unnecessary complexity.

Prefer readable code.

Prefer explicit code over clever code.

Build incrementally.

---

# Cloud-Ready Multi-Sensor Architecture

Signal Observatory should ultimately become a web-based scientific platform for The Invisible Observatory.

The Raspberry Pi will act as an **edge device**, responsible for collecting measurements from connected hardware such as SDRs, cameras, environmental sensors and future scientific instruments.

The primary user interface should be a web application accessible from any device.

The architecture should separate:

- Edge Device (hardware acquisition)
- Backend (processing, APIs and storage)
- Frontend (scientific dashboard)

Initially all services may run on the Raspberry Pi.

As the project grows, components should be easy to migrate to cloud infrastructure.

The long-term vision is to support multiple observatories distributed around the world, all connected to a common backend and unified timeline.

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
Modules: Radio | Cameras | Weather | Solar/UV | Astronomy | Future Sensors
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
- Visible camera
- Raspberry Pi NoIR or NIR-capable camera
- Thermal camera
- UV sensor
- Solar irradiance sensor
- Lightning detector
- Air quality sensors
- Radio astronomy antenna
- Oscilloscope

---

# Development Roadmap

## Phase 0 — Observatory Bring-Up

Verify the Raspberry Pi and hardware signal chain before building application code.

Learn:

- SSH
- Raspberry Pi setup
- USB device detection
- Known-good hardware validation
- Why unknown hardware and unknown software should not be debugged at the same time

---

## Phase 0.5 — Platform Foundation

Before backend implementation hardens, document and later introduce the generic observatory model:

- Observatory
- Device
- Sensor
- CaptureSession
- Measurement
- DerivedMetric
- Observation
- Experiment

The goal is to make sure Phase 1 radio work fits into a multi-sensor platform instead of becoming a standalone SDR-only app.

---

## Phase 1 — Radio Module: Spectrum Analyzer

Build a real-time spectrum analyzer.

Features:

- RTL-SDR integration
- IQ sample acquisition
- FFT
- Spectrum visualization
- Waterfall
- Peak detection
- SQLite logging
- Measurements modeled as radio sensor data inside the generic platform

Learn:

- Sampling
- IQ
- FFT
- Frequency
- Noise
- SNR

---

## Phase 2 — Unified Timeline MVP

Create the first cross-sensor product concept, even if early data is seeded or simulated.

Features:

- Query measurements around a target timestamp
- Display nearby radio measurements and future sensor placeholders
- Show derived metrics and observations connected to evidence
- Establish the pattern for comparing multiple sensors over time

Learn:

- Time-series data modeling
- Timestamp tolerance windows
- Sensor synchronization
- Evidence-linked observations

---

## Phase 3 — Radio Signal Intelligence

- Automatic signal detection
- Signal classification
- Occupancy statistics
- Daily reports
- Noise floor estimation

---

## Phase 4 — ADS-B

Receive aircraft transmissions directly.

Learn packet decoding and radio protocols.

---

## Phase 5 — Weather Satellites

Receive and decode NOAA weather satellite imagery.

---

## Phase 6 — Meteorology

Integrate sensors for:

- Temperature
- Pressure
- Humidity
- Wind
- Rain
- Air quality

---

## Phase 7 — Near-Infrared Plant Observatory

Add the first non-radio module once the generic platform foundation is ready.

Possible hardware:

- RGB camera
- Raspberry Pi NoIR or NIR-capable camera
- Temperature/humidity sensor
- Controlled lighting
- White reference target

Initial experiment:

- Capture visible and NIR images of the same plant over time
- Record environmental context and watering events
- Display images and environmental readings on the Unified Timeline
- Avoid plant-health claims until calibration and validation exist

Learn:

- Imaging sensors
- Reflectance
- Calibration
- Controlled experiments
- Cross-sensor comparison

---

## Phase 8 — Astronomy

Track:

- Sun
- Moon
- ISS
- Planets
- Satellites

Later add amateur radio astronomy.

---

## Phase 9 — Antenna Laboratory

Experiment with antenna gain, polarization, orientation and noise.

---

## Phase 10 — Information Theory

Inspired by Claude Shannon.

Implement visualizations for:

- Entropy
- Bandwidth
- SNR
- Channel capacity

---

## Phase 11 — AI Scientist

Use AI to:

- Detect anomalies
- Discover patterns
- Summarize observations
- Suggest experiments
- Clearly distinguish evidence from speculation
- Link every observation to supporting measurements

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
    vision/
    architecture/
    roadmap/

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
- Build every sensor module before the first module is understood.
- Claim scientific accuracy for uncalibrated optical, thermal, NIR, UV or radio measurements.
- Let AI observations appear without evidence, confidence and uncertainty language.

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
