"""Stable identity types for Evidence artifacts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from idmp.core import EvidenceError

_TYPE_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True, slots=True)
class EvidenceType:
    """Validated, extensible classification of Evidence."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not normalized:
            raise EvidenceError("Evidence type must not be empty.")
        if _TYPE_PATTERN.fullmatch(normalized) is None:
            raise EvidenceError(
                "Evidence type must start with a letter and contain only "
                "lowercase letters, numbers, or hyphens."
            )
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class EvidenceId:
    """Globally unique identity for an Evidence artifact."""

    evidence_type: EvidenceType
    unique_id: UUID

    @classmethod
    def create(cls, evidence_type: EvidenceType) -> EvidenceId:
        return cls(evidence_type=evidence_type, unique_id=uuid4())

    @classmethod
    def parse(cls, raw_value: str) -> EvidenceId:
        parts = raw_value.strip().split("_", maxsplit=2)
        if len(parts) != 3 or parts[0] != "evd":
            raise EvidenceError(
                "Evidence ID must use the form evd_<evidence-type>_<uuid>."
            )

        try:
            evidence_type = EvidenceType(parts[1])
            unique_id = UUID(parts[2])
        except ValueError as error:
            raise EvidenceError("Evidence ID contains an invalid UUID.") from error

        return cls(evidence_type=evidence_type, unique_id=unique_id)

    def __str__(self) -> str:
        return f"evd_{self.evidence_type}_{self.unique_id}"
