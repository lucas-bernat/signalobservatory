# The Invisible Observatory Vision

Signal Observatory began as a radio-frequency learning project. The long-term vision is broader:

> Build a personal scientific observatory that measures phenomena humans cannot directly perceive.

This broader product direction is called **The Invisible Observatory**.

Signal Observatory remains the repository name and first implementation path. The first physical module is radio observation with Raspberry Pi and RTL-SDR hardware. The architecture should, however, grow toward a modular multi-sensor observatory rather than a single-purpose SDR application.

## North Star

The Invisible Observatory should eventually behave like a scientific time machine.

At a recorded moment, the user should be able to inspect nearby measurements from multiple sensors:

```text
18:43:00
+-- Radio spectrum
+-- Visible image
+-- Near-infrared image
+-- Thermal image
+-- Weather measurement
+-- UV / solar measurement
+-- Night-sky image
+-- Human or AI observation
```

Measurements do not need identical timestamps. The system should support time-window queries such as:

```text
target timestamp +/- 30 seconds
```

## Scientific Questions

The platform should help answer questions like:

- What was happening across all sensors at a specific moment?
- How did a measurement change over minutes, hours, days or weeks?
- Are changes in one sensor correlated with changes in another?
- Was an event unusual compared with prior observations?
- What evidence supports an observation or hypothesis?
- What experiment should be run next?

## Sensor Modalities

The platform should be able to add modules over time:

- Radio-frequency signals
- Visible light
- Near-infrared light
- Multispectral and hyperspectral imaging
- Thermal imaging
- Weather and environmental data
- Solar and ultraviolet radiation
- Night-sky and astronomical observations
- AI-generated scientific observations

The immediate goal is not to implement all of these. The goal is to avoid architectural choices that would make them hard later.

## Relationship To Radio

Radio remains the best first module because it teaches:

- sampling
- I/Q data
- frequency
- FFT
- noise floor
- SNR
- antennas
- hardware bring-up
- edge-device acquisition

But radio-specific terms should not define the entire database or API.

Prefer:

```text
Sensor(type="radio")
Measurement(type="radio-spectrum")
DerivedMetric(type="detected-frequency-peak")
Observation(evidence=[measurementId])
```

Avoid making the entire platform depend on names like:

```text
SDRDevice
RadioScan
SpectrumFrame
```

Those may still exist inside the radio module, but not as the core product model.

## Scientific Integrity

The system should clearly distinguish:

- raw measurement
- processed data
- derived metric
- human observation
- AI observation
- speculation
- calibrated result

Measurements from different sensors are not automatically comparable. Calibration metadata matters.

The UI should eventually show whether a measurement is:

- uncalibrated
- partially calibrated
- fully calibrated

For example, near-infrared plant experiments should not claim plant-health diagnosis until sensor bands, lighting, references and calibration have been validated.

## AI Scientist Direction

The AI Scientist should be designed carefully and implemented late.

It may eventually:

- summarize recent measurements
- compare observations with historical baselines
- detect unusual patterns
- suggest possible correlations
- generate experiment ideas

It must:

- link observations to supporting measurements
- report confidence
- distinguish evidence from interpretation
- use uncertainty language such as "observed", "correlated", "may indicate" and "requires further testing"

## Near-Term Product Principle

Build the radio spectrum analyzer as the first module of a generic observatory platform.

Do not slow down Phase 1 by building every future abstraction immediately. But do keep the naming, data model and boundaries compatible with a multi-sensor future.
