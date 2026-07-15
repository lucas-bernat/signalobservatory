"""Source interfaces for Signal Observatory web data.

A source is anything that can produce one measurement frame for the dashboard.
Today that is synthetic data. Later it can be a recorded IQ file, RTL-SDR
samples, or another instrument module.
"""

from __future__ import annotations

from typing import Any, Protocol


SourceMetadata = dict[str, Any]
SpectrumFrame = dict[str, Any]


class SpectrumSource(Protocol):
    """Contract for anything that can produce spectrum dashboard data."""

    name: str

    def metadata(self) -> SourceMetadata:
        """Return descriptive source information for status displays."""

    def snapshot(self) -> SpectrumFrame:
        """Return one current spectrum frame."""
