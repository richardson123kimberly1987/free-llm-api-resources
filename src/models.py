"""Data models and type definitions for free-llm-api-resources.

This module defines the dataclasses and TypedDicts used to represent
providers and their associated models throughout the project.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Model:
    """Represents a single LLM model offered by a provider."""

    name: str
    """The model identifier/name as used in the API."""

    context_window: Optional[int] = None
    """Maximum context window size in tokens, if known."""

    max_output_tokens: Optional[int] = None
    """Maximum number of output tokens, if known."""

    is_free: bool = True
    """Whether the model is available for free (within rate limits)."""

    notes: Optional[str] = None
    """Any additional notes about the model (e.g., deprecation warnings)."""

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Model name must be a non-empty string.")
        if self.context_window is not None and self.context_window <= 0:
            raise ValueError("context_window must be a positive integer.")
        if self.max_output_tokens is not None and self.max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be a positive integer.")


@dataclass
class RateLimit:
    """Represents rate limit information for a provider tier."""

    requests_per_minute: Optional[int] = None
    requests_per_day: Optional[int] = None
    tokens_per_minute: Optional[int] = None
    tokens_per_day: Optional[int] = None

    def is_empty(self) -> bool:
        """Returns True if no rate limit fields are set."""
        return all(
            v is None
            for v in [
                self.requests_per_minute,
                self.requests_per_day,
                self.tokens_per_minute,
                self.tokens_per_day,
            ]
        )

    def __str__(self) -> str:
        parts = []
        if self.requests_per_minute is not None:
            parts.append(f"{self.requests_per_minute} RPM")
        if self.requests_per_day is not None:
            parts.append(f"{self.requests_per_day} RPD")
        if self.tokens_per_minute is not None:
            parts.append(f"{self.tokens_per_minute} TPM")
        if self.tokens_per_day is not None:
            parts.append(f"{self.tokens_per_day} TPD")
        return ", ".join(parts) if parts else "N/A"


@dataclass
class Provider:
    """Represents an API provider offering free LLM access."""

    name: str
    """Display name of the provider."""

    url: str
    """Homepage or signup URL for the provider."""

    api_base: Optional[str] = None
    """Base URL for the API endpoint, if OpenAI-compatible."""

    requires_payment_info: bool = False
    """Whether a credit card or payment method is required to sign up."""

    openai_compatible: bool = True
    """Whether the provider exposes an OpenAI-compatible API."""

    models: list[Model] = field(default_factory=list)
    """List of models available from this provider."""

    rate_limit: Optional[RateLimit] = None
    """Default rate limits applied across models (may vary per model)."""

    notes: Optional[str] = None
    """Any additional notes about the provider."""

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Provider name must be a non-empty string.")
        if not self.url or not self.url.startswith(("http://", "https://")):
            raise ValueError(f"Provider '{self.name}' must have a valid URL.")

    @property
    def free_models(self) -> list[Model]:
        """Returns only the models marked as free."""
        return [m for m in self.models if m.is_free]

    def __repr__(self) -> str:
        return f"Provider(name={self.name!r}, models={len(self.models)})"
