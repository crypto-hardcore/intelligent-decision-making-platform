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
from idmp.core import AssessmentError
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
        statement="BTCUSDT was recorded at 118,000 USDT.",
        observations=(make_observation(),),
    )


def make_assessment(
    *,
    assessment_type: AssessmentType | None = None,
    assessment_id: AssessmentId | None = None,
    created_at: datetime | None = None,
    conclusion: str = "Available evidence supports a bullish market bias.",
    evidence: tuple[Evidence, ...] | None = None,
    confidence: AssessmentConfidence | None = None,
    assumptions: tuple[str, ...] = (
        "The market-price observation is accurate.",
    ),
    limitations: tuple[str, ...] = (
        "Only one evidence artifact is currently available.",
    ),
) -> Assessment:
    resolved_type = assessment_type or AssessmentType("market-bias")
    resolved_id = assessment_id or AssessmentId.create(resolved_type)

    return Assessment(
        assessment_id=resolved_id,
        assessment_type=resolved_type,
        created_at=created_at
        or datetime(2026, 7, 21, 10, 2, tzinfo=UTC),
        conclusion=conclusion,
        evidence=evidence or (make_evidence(),),
        confidence=confidence or AssessmentConfidence(0.75),
        assumptions=assumptions,
        limitations=limitations,
    )


def test_valid_assessment_is_created() -> None:
    assessment = make_assessment()

    assert assessment.assessment_type == AssessmentType("market-bias")
    assert assessment.confidence == AssessmentConfidence(0.75)
    assert len(assessment.evidence) == 1


def test_assessment_conclusion_is_normalized() -> None:
    assessment = make_assessment(
        conclusion="  Evidence supports a bullish market bias.  "
    )

    assert assessment.conclusion == (
        "Evidence supports a bullish market bias."
    )


def test_assessment_id_type_must_match_assessment_type() -> None:
    identifier_type = AssessmentType("market-bias")
    assessment_id = AssessmentId.create(identifier_type)

    with pytest.raises(
        AssessmentError,
        match="Assessment ID type must match the Assessment type",
    ):
        make_assessment(
            assessment_type=AssessmentType("operational-risk"),
            assessment_id=assessment_id,
        )


def test_created_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        AssessmentError,
        match="created_at must be timezone-aware",
    ):
        make_assessment(created_at=datetime(2026, 7, 21, 10, 2))


def test_empty_conclusion_is_rejected() -> None:
    with pytest.raises(
        AssessmentError,
        match="conclusion must not be empty",
    ):
        make_assessment(conclusion="   ")


def test_assessment_requires_at_least_one_evidence_artifact() -> None:
    assessment_type = AssessmentType("market-bias")

    with pytest.raises(
        AssessmentError,
        match="must reference at least one Evidence artifact",
    ):
        Assessment(
            assessment_id=AssessmentId.create(assessment_type),
            assessment_type=assessment_type,
            created_at=datetime(2026, 7, 21, 10, 2, tzinfo=UTC),
            conclusion="Evidence is insufficient.",
            evidence=(),
            confidence=AssessmentConfidence(0.25),
        )


def test_non_evidence_item_is_rejected() -> None:
    with pytest.raises(
        AssessmentError,
        match="must contain only Evidence artifacts",
    ):
        make_assessment(
            evidence=(make_evidence(), "not evidence"),  # type: ignore[arg-type]
        )


def test_duplicate_evidence_is_rejected() -> None:
    evidence = make_evidence()

    with pytest.raises(
        AssessmentError,
        match="must not reference duplicate Evidence artifacts",
    ):
        make_assessment(evidence=(evidence, evidence))


@pytest.mark.parametrize(
    "value",
    [
        -0.01,
        1.01,
        float("inf"),
        float("-inf"),
        float("nan"),
    ],
)
def test_invalid_assessment_confidence_is_rejected(value: float) -> None:
    with pytest.raises(AssessmentError):
        AssessmentConfidence(value)


def test_boolean_confidence_is_rejected() -> None:
    with pytest.raises(
        AssessmentError,
        match="must be a numeric value",
    ):
        AssessmentConfidence(True)


@pytest.mark.parametrize("value", [0.0, 0.5, 1.0])
def test_valid_assessment_confidence_is_accepted(value: float) -> None:
    confidence = AssessmentConfidence(value)

    assert confidence.value == value


def test_assumptions_are_normalized() -> None:
    assessment = make_assessment(
        assumptions=("  Prices are accurate.  ", " Liquidity is normal "),
    )

    assert assessment.assumptions == (
        "Prices are accurate.",
        "Liquidity is normal",
    )


def test_empty_assumption_is_rejected() -> None:
    with pytest.raises(
        AssessmentError,
        match="assumption item must not be empty",
    ):
        make_assessment(assumptions=("Valid assumption.", "   "))


def test_limitations_are_normalized() -> None:
    assessment = make_assessment(
        limitations=("  Limited history.  ", " No order-book evidence "),
    )

    assert assessment.limitations == (
        "Limited history.",
        "No order-book evidence",
    )


def test_empty_limitation_is_rejected() -> None:
    with pytest.raises(
        AssessmentError,
        match="limitation item must not be empty",
    ):
        make_assessment(limitations=("Known limitation.", "   "))


def test_assessment_preserves_referenced_evidence() -> None:
    first_evidence = make_evidence()
    second_evidence = make_evidence()

    assessment = make_assessment(
        evidence=(first_evidence, second_evidence),
    )

    assert assessment.evidence == (
        first_evidence,
        second_evidence,
    )


def test_assessment_is_immutable() -> None:
    assessment = make_assessment()

    with pytest.raises(FrozenInstanceError):
        assessment.conclusion = "Changed."  # type: ignore[misc]