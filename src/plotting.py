"""Shared plotting helpers for figure reproduction."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import scanpy as sc

from .config import FIGURES_DIR, SCANPY_FIGDIR


def setup_scanpy():
    """Apply consistent scanpy / matplotlib defaults."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sc.settings.figdir = SCANPY_FIGDIR
    sc.settings.set_figure_params(dpi=120, facecolor="white", frameon=False)
    plt.rcParams["figure.figsize"] = (6, 5)
    plt.rcParams["font.size"] = 10


def save_figure(name: str, dpi: int = 300) -> Path:
    """Save the current matplotlib figure to figures/."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out = FIGURES_DIR / name
    plt.savefig(out, dpi=dpi, bbox_inches="tight")
    plt.close()
    return out
