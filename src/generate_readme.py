#!/usr/bin/env python3
"""Script to generate README.md from template and data.

This script reads the README_template.md and data.py files,
processes the provider data, and generates the final README.md.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add the src directory to the path so we can import data
sys.path.insert(0, str(Path(__file__).parent))

from data import PROVIDERS, Provider, Model


REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_PATH = Path(__file__).parent / "README_template.md"
OUTPUT_PATH = REPO_ROOT / "README.md"


def format_model_row(model: Model) -> str:
    """Format a single model as a Markdown table row."""
    name = model.name or ""
    context = f"{model.context_window:,}" if model.context_window else "N/A"
    notes = model.notes or ""
    return f"| {name} | {context} | {notes} |"


def format_provider_section(provider: Provider) -> str:
    """Format a provider and its models as a Markdown section."""
    lines = []

    # Provider heading
    lines.append(f"### {provider.name}\n")

    # Provider description / link
    if provider.url:
        lines.append(f"**Website:** [{provider.url}]({provider.url})\n")

    if provider.description:
        lines.append(f"{provider.description}\n")

    # Free tier details
    if provider.free_tier_details:
        lines.append(f"**Free tier:** {provider.free_tier_details}\n")

    # Rate limits
    if provider.rate_limits:
        lines.append(f"**Rate limits:** {provider.rate_limits}\n")

    # Models table
    if provider.models:
        lines.append("| Model | Context Window | Notes |")
        lines.append("|-------|---------------|-------|")
        for model in provider.models:
            lines.append(format_model_row(model))
        lines.append("")

    # Notes / caveats
    if provider.notes:
        lines.append(f"> **Note:** {provider.notes}\n")

    return "\n".join(lines)


def build_provider_table(providers: list[Provider]) -> str:
    """Build a summary table of all providers."""
    lines = [
        "| Provider | Free Models | Rate Limits | Notes |",
        "|----------|-------------|-------------|-------|',
    ]
    for provider in providers:
        name_cell = f"[{provider.name}](#{provider.name.lower().replace(' ', '-')})" if provider.name else ""
        model_count = len(provider.models) if provider.models else 0
        model_cell = str(model_count) if model_count else "N/A"
        rate_cell = provider.rate_limits or "N/A"
        notes_cell = provider.notes or ""
        lines.append(f"| {name_cell} | {model_cell} | {rate_cell} | {notes_cell} |")
    lines.append("")
    return "\n".join(lines)


def render_template(template: str, providers: list[Provider]) -> str:
    """Render the README template with provider data."""
    # Build individual provider sections
    # Sort providers alphabetically by name for consistent ordering
    sorted_providers = sorted(providers, key=lambda p: (p.name or "").lower())

    provider_sections = "\n---\n\n".join(
        format_provider_section(p) for p in sorted_providers
    )

    # Build summary table
    provide
