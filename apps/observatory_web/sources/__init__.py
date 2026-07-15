"""Spectrum source implementations for the observatory web app."""

from .base import SpectrumFrame, SpectrumSource
from .synthetic import SyntheticSpectrumSource


__all__ = ["SpectrumFrame", "SpectrumSource", "SyntheticSpectrumSource"]
