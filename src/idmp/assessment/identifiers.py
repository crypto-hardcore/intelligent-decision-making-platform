"""Stable identity types for Assessment artifacts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from idmp.core import AssessmentError

_TYPE_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True, slots=True)
class AssessmentType:
    """Validated, extensible classification of an Assessment."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise AssessmentError("Assessment type must not be empty.")

        if _TYPE_PATTERN.fullmatch(normalized) is None:
            raise AssessmentError(
                "Assessment type must start with a letter and contain only "
                "lowercase letters, numbers, or hyphens."
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class AssessmentId:
    """Globally unique identity for an Assessment artifact."""

    assessment_type: AssessmentType
    unique_id: UUID

    @classmethod
    def create(cls, assessment_type: AssessmentType) -> AssessmentId:
        return cls(
            assessment_type=assessment_type,
            unique_id=uuid4(),
        )

    @classmethod
    def parse(cls, raw_value: str) -> AssessmentId:
        parts = raw_value.strip().split("_", maxsplit=2)

        if len(parts) != 3 or parts[0] != "asm":
            raise AssessmentError(
                "Assessment ID must use the form asm_<assessment-type>_<uuid>."
            )

        try:
            assessment_type = AssessmentType(parts[1])
            unique_id = UUID(parts[2])
        except ValueError as error:
            raise AssessmentError(
                "Assessment ID contains an invalid UUID."
            ) from error

        return cls(
            assessment_type=assessment_type,
            unique_id=unique_id,
        )

    def __str__(self) -> str:
        return f"asm_{self.assessment_type}_{self.unique_id}"