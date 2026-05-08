"""Validation script for data.py entries.

Checks that all provider entries in data.py conform to expected structure
and contain required fields before README generation.
"""

import sys
from typing import Any

try:
    from data import PROVIDERS
except ImportError:
    print("ERROR: Could not import PROVIDERS from data.py")
    sys.exit(1)


REQUIRED_PROVIDER_FIELDS = {"name", "url", "models"}
REQUIRED_MODEL_FIELDS = {"name"}
OPTIONAL_MODEL_FIELDS = {
    "free_tier",
    "context_window",
    "notes",
    "input_price",
    "output_price",
    "requires_cc",
    "rate_limit",
}


def validate_provider(provider: dict[str, Any], index: int) -> list[str]:
    """Validate a single provider entry.

    Args:
        provider: The provider dictionary to validate.
        index: The index of the provider in the list (for error messages).

    Returns:
        A list of validation error messages. Empty if valid.
    """
    errors = []
    provider_name = provider.get("name", f"<provider at index {index}>")

    # Check required fields
    for field in REQUIRED_PROVIDER_FIELDS:
        if field not in provider:
            errors.append(f"[{provider_name}] Missing required field: '{field}'")

    # Validate URL format
    url = provider.get("url", "")
    if url and not (url.startswith("http://") or url.startswith("https://")):
        errors.append(f"[{provider_name}] URL does not start with http:// or https://: '{url}'")

    # Validate models list
    models = provider.get("models", [])
    if not isinstance(models, list):
        errors.append(f"[{provider_name}] 'models' must be a list, got {type(models).__name__}")
    elif len(models) == 0:
        errors.append(f"[{provider_name}] 'models' list is empty")
    else:
        for model_index, model in enumerate(models):
            model_errors = validate_model(model, provider_name, model_index)
            errors.extend(model_errors)

    return errors


def validate_model(model: dict[str, Any], provider_name: str, index: int) -> list[str]:
    """Validate a single model entry within a provider.

    Args:
        model: The model dictionary to validate.
        provider_name: The name of the parent provider (for error messages).
        index: The index of the model in the list (for error messages).

    Returns:
        A list of validation error messages. Empty if valid.
    """
    errors = []
    model_name = model.get("name", f"<model at index {index}>")

    # Check required fields
    for field in REQUIRED_MODEL_FIELDS:
        if field not in model:
            errors.append(
                f"[{provider_name}][{model_name}] Missing required field: '{field}'"
            )

    # Warn about unknown fields
    known_fields = REQUIRED_MODEL_FIELDS | OPTIONAL_MODEL_FIELDS
    for field in model:
        if field not in known_fields:
            errors.append(
                f"[{provider_name}][{model_name}] Unknown field: '{field}' "
                f"(expected one of: {sorted(known_fields)})"
            )

    # Validate boolean fields
    for bool_field in ("free_tier", "requires_cc"):
        if bool_field in model and not isinstance(model[bool_field], bool):
            errors.append(
                f"[{provider_name}][{model_name}] Field '{bool_field}' must be a bool, "
                f"got {type(model[bool_field]).__name__}"
            )

    return errors


def validate_all(providers: list[dict[str, Any]]) -> tuple[int, int]:
    """Validate all provider entries.

    Args:
        providers: List of provider dictionaries.

    Returns:
        A tuple of (error_count, provider_count).
    """
    all_errors = []

    for index, provider in enumerate(providers):
        errors = validate_provider(provider, index)
        all_errors.extend(errors)

    if all_errors:
        print(f"Found {len(all_errors)} validation error(s):\n")
        for error in all_errors:
            print(f"  ✗ {error}")
        print()
    else:
        print(f"✓ All {len(providers)} provider(s) passed validation.")

    return len(all_errors), len(providers)


if __name__ == "__main__":
    error_count, provider_count = validate_all(PROVIDERS)
    if error_count > 0:
        sys.exit(1)
    print(f"Validated {provider_count} provider(s) successfully.")
