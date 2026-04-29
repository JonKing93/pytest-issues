"""
Validate and parse message inputs
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    Messages = list[str]
    RequireChecks = bool


def validate(messages: tuple) -> tuple[str] | None:
    "Validates user-provided messages args"

    if messages == (None,):
        messages = None
    else:
        for s, string in enumerate(messages):
            if not isinstance(string, str):
                raise TypeError(f"error message[{s}] is not a string")
    return messages


def parse(
    messages: tuple[str, ...] | None,
    format: bool,
    func_kwargs: dict,
) -> tuple[Messages, RequireChecks]:
    "Prepares messages for final validation"

    # Convert to list and optionally disable message checking requirements
    if messages is None:
        require_messages = False
        messages = []
    else:
        require_messages = True
        messages = list(messages)

    # Optionally format messages
    if format:
        messages = [message.format(**func_kwargs) for message in messages]
    return messages, require_messages
