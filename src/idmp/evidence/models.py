"""Canonical Evidence domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from idmp.core import EvidenceError
from idmp.evidence.identifiers import EvidenceId, EvidenceType
from idmp.observation import Observation


def _require_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise EvidenceError(f"{field_name} must not be empty.")
    return normalized


def _require_aware_datetime(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise EvidenceError(f"{field_name} must be timezone-aware.")


@dataclass(frozen=True, slots=True)
class Evidence:
    """Immutable representation of evidence derived from Observation(s)."""

    evidence_id: EvidenceId
    evidence_type: EvidenceType
    created_at: datetime
    statement: str
    observations: tuple[Observation, ...]

    def __post_init__(self) -> None:
        if self.evidence_id.evidence_type != self.evidence_type:
            raise EvidenceError(
                "Evidence ID type must match the Evidence type."
            )

        _require_aware_datetime(self.created_at, "created_at")

        object.__setattr__(
            self,
            "statement",
            _require_text(self.statement, "statement"),
        )

        if not self.observations:
            raise EvidenceError(
                "Evidence must reference at least one Observation."
            )

