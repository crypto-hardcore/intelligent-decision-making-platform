"""Canonical Assessment domain model."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime

from idmp.assessment.identifiers import AssessmentId, AssessmentType
from idmp.core import AssessmentError
from idmp.evidence import Evidence


def _require_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise AssessmentError(f"{field_name} must not be empty.")
    return normalized


def _require_aware_datetime(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise AssessmentError(f"{field_name} must be timezone-aware.")


def _normalize_text_items(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    return tuple(
        _require_text(value, f"{field_name} item")
        for value in values
    )


@dataclass(frozen=True, slots=True)
class AssessmentConfidence:
    """Validated confidence in an Assessment's analytical conclusion."""

    value: float

    def __post_init__(self) -> None:
        if isinstance(self.value, bool):
            raise AssessmentError(
                "Assessment confidence must be a numeric value."
            )

        normalized = float(self.value)

        if not math.isfinite(normalized):
            raise AssessmentError(
                "Assessment confidence must be finite."
            )

        if not 0.0 <= normalized <= 1.0:
            raise AssessmentError(
                "Assessment confidence must be between 0.0 and 1.0."
            )

        object.__setattr__(self, "value", normalized)


@dataclass(frozen=True, slots=True)
class Assessment:
    """Immutable analytical interpretation derived from Evidence."""

    assessment_id: AssessmentId
    assessment_type: AssessmentType
    created_at: datetime
    conclusion: str
    evidence: tuple[Evidence, ...]
    confidence: AssessmentConfidence
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.assessment_id.assessment_type != self.assessment_type:
            raise AssessmentError(
                "Assessment ID type must match the Assessment type."
            )

        _require_aware_datetime(self.created_at, "created_at")

        object.__setattr__(
            self,
            "conclusion",
            _require_text(self.conclusion, "conclusion"),
        )

        normalized_evidence = tuple(self.evidence)
        if not normalized_evidence:
            raise AssessmentError(
                "Assessment must reference at least one Evidence artifact."
            )

        if not all(
            isinstance(item, Evidence)
            for item in normalized_evidence
        ):
            raise AssessmentError(
                "Assessment evidence must contain only Evidence artifacts."
            )

        evidence_ids = {
            item.evidence_id
            for item in normalized_evidence
        }
        if len(evidence_ids) != len(normalized_evidence):
            raise AssessmentError(
                "Assessment must not reference duplicate Evidence artifacts."
            )

        object.__setattr__(self, "evidence", normalized_evidence)
        object.__setattr__(
            self,
            "assumptions",
            _normalize_text_items(self.assumptions, "assumption"),
        )
        object.__setattr__(
            self,
            "limitations",
            _normalize_text_items(self.limitations, "limitation"),
        )