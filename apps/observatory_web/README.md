# Observatory Web App

This is the first browser-based Signal Observatory instrument surface.

It starts with a synthetic spectrum source so the API, frontend, and instrument workflow can be built before the RTL-SDR arrives.

## Scientific Question

Can a browser read synthetic spectrum data from a local instrument server and update the display like a live observatory dashboard?

## Current Architecture

```mermaid
flowchart LR
    A["SpectrumSource interface"] --> B["SyntheticSpectrumSource"]
    B --> C["/api/spectrum"]
    D["Pi or Mac status"] --> E["/api/status"]
    C --> F["Browser UI"]
    E --> F
    F --> G["Canvas spectrum and waveform"]
```

The important design idea is that the UI reads a data shape, not a hardware-specific driver. A source only has to produce one current spectrum frame.

Later:

```text
SyntheticSpectrumSource
RecordedIqSpectrumSource
RtlSdrSpectrumSource
```

The web UI should not need to know which source created the spectrum frame.

## Source Modules

```text
apps/observatory_web/sources/
  base.py       # SpectrumSource contract
  dsp.py        # dependency-free FFT helper
  synthetic.py  # current synthetic two-tone source
```

## Run On The Mac

From the repository root:

```bash
python3 apps/observatory_web/server.py
```

Open:

```text
http://127.0.0.1:8000
```

## Run On The Raspberry Pi Later

When your Mac and Raspberry Pi are back on the same local network:

```bash
cd ~/Code/signalobservatory
git pull
python3 apps/observatory_web/server.py --host 0.0.0.0 --port 8000
```

Then open this from your Mac browser:

```text
http://signal-observatory.local:8000
```

## API Endpoints

```text
GET /api/status
GET /api/spectrum
```

`/api/status` returns host and runtime information.

`/api/spectrum` returns:

- synthetic signal source name
- sample rate
- FFT size
- bin spacing
- expected tones
- detected peaks
- time-domain waveform points
- frequency-domain spectrum bins

## What To Notice

- The browser refreshes data every second.
- The time-domain waveform is one mixed signal.
- The spectrum separates that signal into frequency peaks.
- The 1 kHz tone appears stronger than the 10 kHz tone.
- This is the same mental model a live SDR spectrum analyzer will use.

## Next Steps

1. Add a recorded IQ file source using the same `SpectrumSource` contract.
2. Add source selection to the server config.
3. Replace polling with WebSockets once the data shape feels stable.
4. Add a waterfall view.
