from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from idmp.assessment import (
    Assessment,
    AssessmentConfidence,
    AssessmentId,
    AssessmentType,
)
from idmp.core import DecisionError
from idmp.decision import (
    Decision,
    DecisionId,
    DecisionStatus,
    DecisionType,
)
from idmp.evidence import Evidence, EvidenceId, EvidenceType
from idmp.observation import (
    DataQuality,
    Observation,
    ObservationId,
    ObservationType,
    Provenance,
)


def make_observation() -> Observation:
    observation_type = ObservationType("price")

    return Observation(
        observation_id=ObservationId.create(observation_type),
        observation_type=observation_type,
        observed_at=datetime(2026, 7, 21, 10, 0, tzinfo=UTC),
        recorded_at=datetime(2026, 7, 21, 10, 0, 1, tzinfo=UTC),
        subject="BTCUSDT",
        value={"price": 118_000.0},
        provenance=Provenance(
            source="Binance Futures",
            collection_method="REST API",
            collector="binance-connector",
            source_record_id="trade-123",
        ),
        data_quality=DataQuality(is_complete=True),
        unit="USDT",
    )


def make_evidence() -> Evidence:
    evidence_type = EvidenceType("market-context")

    return Evidence(
        evidence_id=EvidenceId.create(evidence_type),
        evidence_type=evidence_type,
        created_at=datetime(2026, 7, 21, 10, 1, tzinfo=UTC),
        statement="BTCUSDT traded at 118,000 USDT.",
        observations=(make_observation(),),
    )


def make_assessment() -> Assessment:
    assessment_type = AssessmentType("market-bias")

    return Assessment(
        assessment_id=AssessmentId.create(assessment_type),
        assessment_type=assessment_type,
        created_at=datetime(2026, 7, 21, 10, 2, tzinfo=UTC),
        conclusion="Evidence supports a bullish market bias.",
        evidence=(make_evidence(),),
        confidence=AssessmentConfidence(0.80),
    )


def make_decision(
    *,
    decision_type: DecisionType | None = None,
    decision_id: DecisionId | None = None,
    created_at: datetime | None = None,
    proposed_action: str = "Open a long position.",
    rationale: str = "Bullish assessment exceeds confidence threshold.",
    supporting_assessments: tuple[Assessment, ...] | None = None,
    constraints: tuple[str, ...] = (
        "Maximum portfolio risk remains below policy limits.",
    ),
    status: DecisionStatus = DecisionStatus.PROPOSED,
) -> Decision:
    resolved_type = decision_type or DecisionType("enter-position")
    resolved_id = decision_id or DecisionId.create(resolved_type)

    return Decision(
        decision_id=resolved_id,
        decision_type=resolved_type,
        created_at=created_at
        or datetime(2026, 7, 21, 10, 3, tzinfo=UTC),
        proposed_action=proposed_action,
        rationale=rationale,
        supporting_assessments=(
            supporting_assessments
            or (make_assessment(),)
        ),
        constraints=constraints,
        status=status,
    )


def test_valid_decision_is_created() -> None:
    decision = make_decision()

    assert decision.status is DecisionStatus.PROPOSED
    assert decision.decision_type == DecisionType("enter-position")
    assert len(decision.supporting_assessments) == 1


def test_proposed_action_is_normalized() -> None:
    decision = make_decision(
        proposed_action="  Open a long position.  "
    )

    assert decision.proposed_action == "Open a long position."


def test_rationale_is_normalized() -> None:
    decision = make_decision(
        rationale="  Strong bullish evidence.  "
    )

    assert decision.rationale == "Strong bullish evidence."


def test_decision_id_type_must_match_decision_type() -> None:
    identifier_type = DecisionType("enter-position")
    decision_id = DecisionId.create(identifier_type)

    with pytest.raises(
        DecisionError,
        match="Decision ID type must match the Decision type",
    ):
        make_decision(
            decision_type=DecisionType("exit-position"),
            decision_id=decision_id,
        )


def test_created_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        DecisionError,
        match="created_at must be timezone-aware",
    ):
        make_decision(
            created_at=datetime(2026, 7, 21, 10, 3)
        )


def test_empty_proposed_action_is_rejected() -> None:
    with pytest.raises(
        DecisionError,
        match="proposed_action must not be empty",
    ):
        make_decision(proposed_action="   ")


def test_empty_rationale_is_rejected() -> None:
    with pytest.raises(
        DecisionError,
        match="rationale must not be empty",
    ):
        make_decision(rationale="   ")


def test_decision_requires_at_least_one_assessment() -> None:
    decision_type = DecisionType("enter-position")

    with pytest.raises(
        DecisionError,
        match="must reference at least one Assessment artifact",
    ):
        Decision(
            decision_id=DecisionId.create(decision_type),
            decision_type=decision_type,
            created_at=datetime(2026, 7, 21, 10, 3, tzinfo=UTC),
            proposed_action="Open long.",
            rationale="Bullish evidence.",
            supporting_assessments=(),
        )


def test_non_assessment_item_is_rejected() -> None:
    with pytest.raises(
        DecisionError,
        match="must contain only Assessment artifacts",
    ):
        make_decision(
            supporting_assessments=(
                make_assessment(),
                "invalid",  # type: ignore[arg-type]
            ),
        )


def test_duplicate_assessment_is_rejected() -> None:
    assessment = make_assessment()

    with pytest.raises(
        DecisionError,
        match="must not reference duplicate Assessment artifacts",
    ):
        make_decision(
            supporting_assessments=(
                assessment,
                assessment,
            ),
        )


def test_constraints_are_normalized() -> None:
    decision = make_decision(
        constraints=(
            "  Risk policy satisfied.  ",
            " Liquidity is sufficient ",
        )
    )

    assert decision.constraints == (
        "Risk policy satisfied.",
        "Liquidity is sufficient",
    )


def test_empty_constraint_is_rejected() -> None:
    with pytest.raises(
        DecisionError,
        match="constraint item must not be empty",
    ):
        make_decision(
            constraints=(
                "Valid constraint.",
                "   ",
            )
        )


def test_new_decision_must_be_proposed() -> None:
    with pytest.raises(
        DecisionError,
        match="must have PROPOSED status",
    ):
        make_decision(
            status="approved",  # type: ignore[arg-type]
        )


def test_decision_is_immutable() -> None:
    decision = make_decision()

    with pytest.raises(FrozenInstanceError):
        decision.rationale = "Modified."  # type: ignore[misc]