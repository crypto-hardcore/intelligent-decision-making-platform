"""Canonical Decision domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from idmp.assessment import Assessment
from idmp.core import DecisionError
from idmp.decision.identifiers import DecisionId, DecisionType


def _require_text(value: str, field_name: str) -> str:
    normalized = value.strip()

    if not normalized:
        raise DecisionError(f"{field_name} must not be empty.")

    return normalized


def _require_aware_datetime(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise DecisionError(f"{field_name} must be timezone-aware.")


def _normalize_text_items(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    return tuple(
        _require_text(value, f"{field_name} item")
        for value in values
    )


class DecisionStatus(StrEnum):
    """Lifecycle status of an immutable Decision proposal."""

    PROPOSED = "proposed"


@dataclass(frozen=True, slots=True)
class Decision:
    """Immutable proposed course of action supported by Assessments."""

    decision_id: DecisionId
    decision_type: DecisionType
    created_at: datetime
    proposed_action: str
    rationale: str
    supporting_assessments: tuple[Assessment, ...]
    constraints: tuple[str, ...] = ()
    status: DecisionStatus = DecisionStatus.PROPOSED

    def __post_init__(self) -> None:
        if self.decision_id.decision_type != self.decision_type:
            raise DecisionError(
                "Decision ID type must match the Decision type."
            )

        _require_aware_datetime(self.created_at, "created_at")

        object.__setattr__(
            self,
            "proposed_action",
            _require_text(self.proposed_action, "proposed_action"),
        )
        object.__setattr__(
            self,
            "rationale",
            _require_text(self.rationale, "rationale"),
        )

        normalized_assessments = tuple(self.supporting_assessments)

        if not normalized_assessments:
            raise DecisionError(
                "Decision must reference at least one Assessment artifact."
            )

        if not all(
            isinstance(item, Assessment)
            for item in normalized_assessments
        ):
            raise DecisionError(
                "Decision supporting assessments must contain only "
                "Assessment artifacts."
            )

        assessment_ids = {
            item.assessment_id
            for item in normalized_assessments
        }

        if len(assessment_ids) != len(normalized_assessments):
            raise DecisionError(
                "Decision must not reference duplicate Assessment artifacts."
            )

        if self.status is not DecisionStatus.PROPOSED:
            raise DecisionError(
                "A newly created Decision must have PROPOSED status."
            )

        object.__setattr__(
            self,
            "supporting_assessments",
            normalized_assessments,
        )
        object.__setattr__(
            self,
            "constraints",
            _normalize_text_items(self.constraints, "constraint"),
        )