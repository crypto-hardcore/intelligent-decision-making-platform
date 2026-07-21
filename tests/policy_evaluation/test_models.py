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
from idmp.core import PolicyEvaluationError
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
from idmp.policy import (
    Policy,
    PolicyId,
    PolicyStatus,
    PolicyType,
)
from idmp.policy_evaluation import (
    PolicyEvaluation,
    PolicyEvaluationId,
    PolicyEvaluationResult,
    PolicyEvaluationType,
)


def make_observation() -> Observation:
    observation_type = ObservationType("price")

    return Observation(
        observation_id=ObservationId.create(observation_type),
        observation_type=observation_type,
        observed_at=datetime(2026, 7, 21, 10, 0, tzinfo=UTC),
        recorded_at=datetime(
            2026,
            7,
            21,
            10,
            0,
            1,
            tzinfo=UTC,
        ),
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
        created_at=datetime(
            2026,
            7,
            21,
            10,
            1,
            tzinfo=UTC,
        ),
        statement="BTCUSDT traded at 118,000 USDT.",
        observations=(make_observation(),),
    )


def make_assessment() -> Assessment:
    assessment_type = AssessmentType("market-bias")

    return Assessment(
        assessment_id=AssessmentId.create(assessment_type),
        assessment_type=assessment_type,
        created_at=datetime(
            2026,
            7,
            21,
            10,
            2,
            tzinfo=UTC,
        ),
        conclusion="Evidence supports a bullish market bias.",
        evidence=(make_evidence(),),
        confidence=AssessmentConfidence(0.80),
    )


def make_decision() -> Decision:
    decision_type = DecisionType("enter-position")

    return Decision(
        decision_id=DecisionId.create(decision_type),
        decision_type=decision_type,
        created_at=datetime(
            2026,
            7,
            21,
            10,
            3,
            tzinfo=UTC,
        ),
        proposed_action="Open a long position.",
        rationale=(
            "Bullish assessment exceeds confidence threshold."
        ),
        supporting_assessments=(make_assessment(),),
        constraints=(
            "Maximum portfolio risk remains below policy limits.",
        ),
        status=DecisionStatus.PROPOSED,
    )


def make_policy(
    *,
    status: PolicyStatus = PolicyStatus.ACTIVE,
) -> Policy:
    policy_type = PolicyType("maximum-risk")

    return Policy(
        policy_id=PolicyId.create(policy_type),
        policy_type=policy_type,
        created_at=datetime(
            2026,
            7,
            21,
            10,
            4,
            tzinfo=UTC,
        ),
        name="Maximum Risk",
        description="Limit position risk.",
        version="1.0",
        status=status,
    )


def make_evaluation(
    *,
    result: PolicyEvaluationResult = (
        PolicyEvaluationResult.PASSED
    ),
    violations: tuple[str, ...] = (),
    warnings: tuple[str, ...] = (),
    explanation: str = "Risk is within limits.",
    policy: Policy | None = None,
) -> PolicyEvaluation:
    evaluation_type = PolicyEvaluationType(
        "decision-compliance"
    )

    return PolicyEvaluation(
        policy_evaluation_id=PolicyEvaluationId.create(
            evaluation_type
        ),
        policy_evaluation_type=evaluation_type,
        evaluated_at=datetime(
            2026,
            7,
            21,
            10,
            5,
            tzinfo=UTC,
        ),
        decision=make_decision(),
        policy=policy or make_policy(),
        result=result,
        explanation=explanation,
        violations=violations,
        warnings=warnings,
    )


def test_valid_passed_policy_evaluation() -> None:
    evaluation = make_evaluation()

    assert evaluation.result is PolicyEvaluationResult.PASSED


def test_valid_failed_policy_evaluation() -> None:
    evaluation = make_evaluation(
        result=PolicyEvaluationResult.FAILED,
        violations=("Risk exceeded.",),
        explanation="Risk exceeds policy.",
    )

    assert evaluation.result is PolicyEvaluationResult.FAILED


def test_valid_not_applicable_policy_evaluation() -> None:
    evaluation = make_evaluation(
        result=PolicyEvaluationResult.NOT_APPLICABLE,
        explanation="Policy does not apply.",
    )

    assert (
        evaluation.result
        is PolicyEvaluationResult.NOT_APPLICABLE
    )


def test_explanation_is_normalized() -> None:
    evaluation = make_evaluation(
        explanation="  Risk is acceptable.  "
    )

    assert evaluation.explanation == "Risk is acceptable."


def test_empty_explanation_is_rejected() -> None:
    with pytest.raises(
        PolicyEvaluationError,
        match="explanation must not be empty",
    ):
        make_evaluation(
            explanation="   ",
        )


def test_failed_evaluation_requires_violation() -> None:
    with pytest.raises(
        PolicyEvaluationError,
        match="failed PolicyEvaluation",
    ):
        make_evaluation(
            result=PolicyEvaluationResult.FAILED,
            violations=(),
        )


def test_passed_evaluation_cannot_have_violations() -> None:
    with pytest.raises(
        PolicyEvaluationError,
        match="Only a failed PolicyEvaluation",
    ):
        make_evaluation(
            violations=("Violation",),
        )


def test_not_applicable_cannot_have_violations() -> None:
    with pytest.raises(
        PolicyEvaluationError,
        match="Only a failed PolicyEvaluation",
    ):
        make_evaluation(
            result=PolicyEvaluationResult.NOT_APPLICABLE,
            violations=("Violation",),
        )


def test_duplicate_violations_are_rejected() -> None:
    with pytest.raises(
        PolicyEvaluationError,
        match="violations must not contain duplicates",
    ):
        make_evaluation(
            result=PolicyEvaluationResult.FAILED,
            violations=("Risk", "Risk"),
        )


def test_duplicate_warnings_are_rejected() -> None:
    with pytest.raises(
        PolicyEvaluationError,
        match="warnings must not contain duplicates",
    ):
        make_evaluation(
            warnings=("Warning", "Warning"),
        )


def test_deprecated_policy_is_allowed() -> None:
    evaluation = make_evaluation(
        policy=make_policy(
            status=PolicyStatus.DEPRECATED
        ),
    )

    assert evaluation.policy.status is PolicyStatus.DEPRECATED


def test_policy_evaluation_is_immutable() -> None:
    evaluation = make_evaluation()

    with pytest.raises(FrozenInstanceError):
        evaluation.explanation = (  # type: ignore[misc]
            "Modified"
        )