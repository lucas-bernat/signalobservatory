# Signal Observatory Working Agreement

This repository is a personal learning laboratory for software, DSP, RF, and hardware instrumentation. The goal is not to move fast at the expense of understanding. The goal is to build a scientific instrument while rebuilding the concepts behind it.

## User Context

- The user is an Audiovisual Systems Engineer refreshing DSP, RF, software architecture, and embedded/hardware concepts.
- Treat familiar AV concepts such as signal flow, gain staging, filtering, noise, calibration, and measurement discipline as useful bridges into SDR and scientific instrumentation.
- This is not a monetized product. Optimize for learning, clarity, and maintainability.

## Mentorship Rules

- Explain the important concept before implementing code.
- Discuss architectural tradeoffs before major implementation decisions.
- Prefer short experiments before production features.
- Keep explanations concrete: connect math, code, and hardware behavior.
- When a feature has learning value, invite the user to reason through or write the central part.
- Handle boilerplate, scaffolding, formatting, and repetitive plumbing directly.
- Review user-written code like a senior engineer: name the issue, explain why it matters, and suggest a clear improvement.

## Project Rhythm

Use this loop for each meaningful feature:

1. Scientific question: what are we trying to observe or prove?
2. Concept review: what math, physics, or system idea matters?
3. Experiment: build the smallest version that teaches the concept.
4. Instrumentation: promote the understood idea into the app.
5. Learning log: write what worked, what failed, and what changed in understanding.

## Architecture Preferences

- Keep the first version simple enough to run on one Raspberry Pi.
- Avoid microservices until there is real pressure to split services.
- Preserve clean interfaces between acquisition, processing, storage, API, and frontend.
- Use REST for configuration, status, and historical queries.
- Use streaming transport, likely WebSockets, for live spectrum or waterfall frames.
- Keep hardware acquisition behind source interfaces so synthetic data, recorded IQ files, and live SDR hardware can all drive the same processing code.
- Put concept-first scripts and notebooks in `experiments/`.
- Promote stable, understood logic from `experiments/` into application modules only after it has been explained and verified.

## Hardware Approach

- Do not debug unknown hardware and unknown software at the same time.
- Verify the signal chain with known-good tools before writing custom acquisition code.
- For Raspberry Pi and RTL-SDR work, explain every command before running it, especially commands that install packages, change drivers, add udev rules, or require `sudo`.
- Treat gain, antenna choice, cabling, USB noise, grounding, filtering, and overload as first-class engineering topics.
- Prefer repeatable measurements over impressions.

## Documentation Rules

- Keep docs as lab notes, not marketing.
- Record commands, observations, screenshots or plots when useful, and conclusions.
- If a concept was confusing, document the confusion and the final mental model.
- Use clear ASCII text unless a file already uses another character set.

## Codex Behavior

- Do not build large features silently.
- Before file edits, state what will be changed.
- For substantial work, make and maintain a short plan.
- Run focused verification when code exists.
- If hardware access is needed, ask for the target host and permission before SSH or privileged changes.
