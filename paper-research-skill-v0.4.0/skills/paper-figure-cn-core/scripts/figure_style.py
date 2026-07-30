from __future__ import annotations

from pathlib import Path


PALETTE = {"ink": "#172033", "teal": "#0F766E", "gold": "#B7791F", "red": "#B42318", "gray": "#6B7280"}


def save_figure(figure: object, output: Path) -> None:
    """Save a matplotlib-like figure with a vector companion and a PNG preview."""
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output.with_suffix(".svg"), bbox_inches="tight")
    figure.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
