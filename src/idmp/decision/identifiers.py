"""Identifiers for the Decision domain."""

from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from idmp.core import DecisionError


_DECISION_TYPE_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True, slots=True)
class DecisionType:
    """Validated Decision classification."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise DecisionError("Decision type must not be empty.")

        if not _DECISION_TYPE_PATTERN.fullmatch(normalized):
            raise DecisionError(
                "Decision type must start with a lowercase letter and contain "
                "only lowercase letters, digits, and hyphens."
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class DecisionId:
    """Globally unique identifier for a Decision."""

    decision_type: DecisionType
    value: UUID

    @classmethod
    def create(cls, decision_type: DecisionType) -> DecisionId:
        """Create a new Decision identifier."""

        return cls(
            decision_type=decision_type,
            value=uuid4(),
        )

    @classmethod
    def parse(cls, raw_value: str) -> DecisionId:
        """Parse a serialized Decision identifier."""

        prefix = "dec_"

        if not raw_value.startswith(prefix):
            raise DecisionError(
                "Decision identifier must start with 'dec_'."
            )

        identifier_body = raw_value[len(prefix) :]
        decision_type_value, separator, uuid_value = (
            identifier_body.rpartition("_")
        )

        if not separator or not decision_type_value or not uuid_value:
            raise DecisionError("Invalid Decision identifier format.")

        try:
            decision_type = DecisionType(decision_type_value)
            parsed_uuid = UUID(uuid_value)
        except (DecisionError, ValueError) as error:
            raise DecisionError(
                "Invalid Decision identifier format."
            ) from error

        return cls(
            decision_type=decision_type,
            value=parsed_uuid,
        )

    def __str__(self) -> str:
        return f"dec_{self.decision_type}_{self.value}"