# Invisible Observatory Roadmap

This roadmap updates the original radio-first plan without abandoning it.

## Guiding Idea

Build the first real instrument with radio, but design the platform so radio becomes one module inside a larger multi-sensor observatory.

```text
Phase 0: prove hardware path
Phase 1: radio module
Later: add non-radio modules and unified timeline
```

## Phase 0: Observatory Bring-Up

Status: current near-term hardware phase.

Goals:

- Raspberry Pi setup
- SSH access
- RTL-SDR detection when the dongle arrives
- known-good SDR tools before custom code
- learning-log notes

## Phase 0.5: Platform Foundation Decisions

Status: documentation/planning only for now.

Goals:

- agree that the core model is Observatory, Device, Sensor, CaptureSession, Measurement, DerivedMetric, Observation and Experiment
- avoid naming the whole backend around radio-only concepts
- decide how radio measurements fit into generic measurements
- identify the smallest schema needed when backend work begins

Do not build a heavy platform layer before we have a real first module.

## Phase 1: Radio Module - Spectrum Analyzer

Status: first software/hardware module.

Goals:

- synthetic I/Q experiments
- recorded IQ experiments
- live RTL-SDR acquisition
- FFT
- spectrum visualization
- waterfall
- peak detection
- initial measurement logging

Important architecture rule:

Radio logic lives in the radio module. Shared storage should use generic measurement concepts.

## Phase 2: Unified Timeline MVP

Status: planned after initial radio measurement logging.

Goals:

- query measurements near a target timestamp
- show radio data and seeded/demo non-radio measurements
- display observations linked to evidence
- prove the cross-sensor time-machine concept

## Phase 3: Radio Signal Intelligence

Goals:

- automatic signal detection
- occupancy statistics
- noise floor estimation
- daily summaries
- simple classification experiments

## Phase 4: ADS-B And Weather Satellites

Goals:

- ADS-B packet reception
- aircraft observation records
- NOAA weather satellite reception
- satellite pass timing and Doppler concepts

## Phase 5: Near-Infrared Plant Observatory

This is the recommended first non-radio module.

Goals:

- visible image capture
- NIR image capture
- environmental context
- controlled lighting notes
- calibration notes
- timeline comparison

Important scientific rule:

Do not claim plant-health diagnosis until calibration and validation exist.

## Later Phases

- weather station
- thermal imaging
- solar and UV monitoring
- sky observatory
- antenna laboratory
- information theory visualizations
- AI scientist

## What Has Changed

Original project:

```text
radio-first observatory
```

Updated project:

```text
multi-sensor observatory, radio-first implementation
```

The next implementation step is still Phase 0 hardware bring-up and Phase 1 radio learning. The difference is that backend, database and API design should be prepared for multiple sensors from the beginning.
