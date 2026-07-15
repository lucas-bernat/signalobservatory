"""Spectrum source implementations for the observatory web app."""

from .base import SourceMetadata, SpectrumFrame, SpectrumSource
from .synthetic import SyntheticSpectrumSource


__all__ = ["SourceMetadata", "SpectrumFrame", "SpectrumSource", "SyntheticSpectrumSource"]
