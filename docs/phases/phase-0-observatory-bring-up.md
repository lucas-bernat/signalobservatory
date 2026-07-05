# Phase 0: Observatory Bring-Up

Phase 0 exists before the PRD roadmap. Its purpose is to prove that the hardware signal chain works before custom software is introduced.

The lesson is simple: do not debug new hardware and new software at the same time.

## Goal

Confirm that the Raspberry Pi, RTL-SDR Blog V4, antenna, drivers, and operating environment can receive known signals using known-good tools.

Only after this phase should the project move into custom IQ capture, FFT processing, and live spectrum visualization.

## Success Criteria

- Raspberry Pi boots reliably and is reachable over SSH.
- RTL-SDR appears as a USB device.
- Kernel messages show the SDR attaching without obvious errors.
- The correct RTL-SDR Blog V4 compatible driver stack is installed and verified.
- `rtl_test` runs without severe sample loss under normal settings.
- At least one known signal is observed with existing SDR tooling.
- Basic notes are recorded in the learning log.

## Hardware Inventory

- Raspberry Pi 5
- RTL-SDR Blog V4
- Antenna
- USB cable or direct USB connection
- Mac development machine
- SSH access to the Pi

Add serial numbers, hostnames, OS versions, and antenna details once known.

## Bring-Up Checklist

### 1. Establish Pi Access

Questions:

- What is the Pi hostname or IP address?
- What OS image and version is it running?
- Is SSH enabled?
- Is the Pi powered by a stable supply?

Useful checks:

```bash
ssh <user>@<pi-host>
uname -a
cat /etc/os-release
```

Concepts to review:

- Edge device vs. development machine
- Why stable power matters for USB peripherals
- Why remote access should be verified before hardware debugging

### 2. Confirm USB Detection

Useful checks:

```bash
lsusb
dmesg
```

What to learn:

- USB enumeration
- Vendor/product IDs
- Difference between "device is visible" and "device is usable"

Expected outcome:

- The RTL-SDR appears in `lsusb`.
- Recent `dmesg` output does not show repeated disconnects, power errors, or driver conflicts.

### 3. Verify Driver Stack

The RTL-SDR Blog V4 has driver requirements that should be verified against the current RTL-SDR Blog documentation before installing packages. Do not assume the default distribution package is correct.

Useful checks after installation:

```bash
rtl_test
rtl_test -t
```

What to learn:

- Kernel drivers vs. user-space SDR libraries
- Why "the command runs" is not the same as "the measurements are correct"
- Sample drops and what they imply about USB throughput, CPU load, or driver issues

### 4. Receive a Known Signal With Existing Tools

Use known-good SDR software before writing custom code.

Candidate signals:

- Local FM broadcast stations
- ADS-B at 1090 MHz, if antenna and location allow
- NOAA weather radio, if available in the region

Candidate tools:

- `rtl_power`
- `rtl_fm`
- SDR++ or GQRX on the Mac
- Other established SDR tooling

What to learn:

- Center frequency
- Sample rate
- RF gain
- Antenna length and band suitability
- Noise floor and overload

### 5. Record the Baseline

Create a learning-log entry with:

- Date and location
- Hardware used
- OS and driver notes
- Commands run
- Known signals observed
- Problems encountered
- Open questions

## Phase 0 Exit Questions

Before moving to Phase 1, answer these in your own words:

- What does the RTL-SDR hardware actually sample?
- Why do we need I/Q data instead of ordinary real-valued audio samples?
- What does sample rate limit?
- What does RF gain change?
- What is one symptom of front-end overload?
- What evidence do we have that the hardware path works?

## Next Phase

Phase 1 should begin with synthetic and recorded data before live application code:

1. Generate a synthetic complex sinusoid.
2. FFT it offline and inspect bins.
3. Capture a short IQ file from the RTL-SDR.
4. FFT the captured file offline.
5. Only then build real-time acquisition and visualization.
