# core/formatters.py
"""Output formatters: tables, heatmaps, sparklines, INR formatting."""

import io
from typing import Sequence

import pandas as pd
from rich.console import Console
from rich.table import Table


SPARK_CHARS = "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"


def sparkline(data: Sequence[float | int]) -> str:
    """Generate an ASCII sparkline from a sequence of numbers."""
    if not data:
        return ""
    mn, mx = min(data), max(data)
    rng = mx - mn if mx != mn else 1
    return "".join(SPARK_CHARS[min(int((v - mn) / rng * (len(SPARK_CHARS) - 1)), len(SPARK_CHARS) - 1)] for v in data)


def heatmap_color(value: float) -> str:
    """Return ANSI color code based on value (green=positive, red=negative)."""
    if value > 0:
        return f"\033[32m{value:+.2f}\033[0m"
    elif value < 0:
        return f"\033[31m{value:+.2f}\033[0m"
    return f"{value:.2f}"


def format_table(df: pd.DataFrame, fmt: str = "markdown", title: str = "") -> str:
    """Format a DataFrame as a table string.

    Args:
        df: Data to format.
        fmt: 'markdown' or 'rich'.
        title: Optional table title.
    """
    if fmt == "markdown":
        return df.to_markdown(index=False)

    # Rich table
    console = Console(file=io.StringIO(), force_terminal=True, width=120)
    table = Table(title=title, show_lines=True)
    for col in df.columns:
        table.add_column(str(col))
    for _, row in df.iterrows():
        table.add_row(*[str(v) for v in row])
    console.print(table)
    return console.file.getvalue()


def format_inr(amount: float) -> str:
    """Format a number in Indian numbering system (lakhs, crores).
    Example: 1500000 -> '15,00,000'
    """
    is_negative = amount < 0
    amount = abs(amount)

    # Split into integer and decimal parts
    if isinstance(amount, float) and amount != int(amount):
        int_part = int(amount)
        dec_part = f".{f'{amount:.2f}'.split('.')[1]}"
    else:
        int_part = int(amount)
        dec_part = ""

    s = str(int_part)
    if len(s) <= 3:
        result = s
    else:
        result = s[-3:]
        s = s[:-3]
        while s:
            result = s[-2:] + "," + result
            s = s[:-2]

    return ("-" if is_negative else "") + result + dec_part


def format_crores(amount: float) -> str:
    """Format amount in crores. Example: 15000000 -> '1.50 Cr'"""
    return f"{amount / 10000000:.2f} Cr"


def format_percent(value: float, already_pct: bool = False) -> str:
    """Format as percentage string.

    Args:
        value: The value to format. By default treated as a decimal (0.156 -> '15.60%').
        already_pct: If True, value is already a percentage (15.6 -> '15.60%').
    """
    if already_pct:
        return f"{value:.2f}%"
    return f"{value * 100:.2f}%"


def narrative_summary(template: str, **kwargs) -> str:
    """Generate a narrative summary from a template and data."""
    return template.format(**kwargs)
