from __future__ import annotations

import pytest

from idmp.core import PolicyEvaluationError
from idmp.policy_evaluation import (
    PolicyEvaluationId,
    PolicyEvaluationType,
)


def test_policy_evaluation_type_is_normalized() -> None:
    evaluation_type = PolicyEvaluationType(
        " Decision-Compliance "
    )

    assert evaluation_type.value == "decision-compliance"


def test_policy_evaluation_type_string_representation() -> None:
    evaluation_type = PolicyEvaluationType(
        "decision-compliance"
    )

    assert str(evaluation_type) == "decision-compliance"


def test_policy_evaluation_type_must_not_be_empty() -> None:
    with pytest.raises(
        PolicyEvaluationError,
        match="Policy evaluation type must not be empty",
    ):
        PolicyEvaluationType("   ")


@pytest.mark.parametrize(
    "value",
    [
        "123evaluation",
        "decision_compliance",
        "decision compliance",
        "decision!",
        "-decision-compliance",
    ],
)
def test_invalid_policy_evaluation_type_is_rejected(
    value: str,
) -> None:
    with pytest.raises(PolicyEvaluationError):
        PolicyEvaluationType(value)


def test_create_policy_evaluation_id() -> None:
    evaluation_type = PolicyEvaluationType(
        "decision-compliance"
    )

    evaluation_id = PolicyEvaluationId.create(
        evaluation_type
    )

    assert (
        evaluation_id.policy_evaluation_type
        == evaluation_type
    )


def test_policy_evaluation_id_string_representation() -> None:
    evaluation_type = PolicyEvaluationType(
        "decision-compliance"
    )
    evaluation_id = PolicyEvaluationId.create(
        evaluation_type
    )

    assert str(evaluation_id) == (
        "peval_decision-compliance_"
        f"{evaluation_id.value}"
    )


def test_parse_policy_evaluation_id_round_trip() -> None:
    original = PolicyEvaluationId.create(
        PolicyEvaluationType("decision-compliance")
    )

    parsed = PolicyEvaluationId.parse(str(original))

    assert parsed == original


def test_parse_preserves_policy_evaluation_type() -> None:
    original = PolicyEvaluationId.create(
        PolicyEvaluationType("risk-compliance")
    )

    parsed = PolicyEvaluationId.parse(str(original))

    assert parsed.policy_evaluation_type == (
        PolicyEvaluationType("risk-compliance")
    )


@pytest.mark.parametrize(
    "raw_value",
    [
        "",
        "abc",
        "peval_decision-compliance",
        "peval__123",
        "peval_decision-compliance_not-a-uuid",
        (
            "pol_decision-compliance_"
            "00000000-0000-0000-0000-000000000000"
        ),
        (
            "peval_123evaluation_"
            "00000000-0000-0000-0000-000000000000"
        ),
    ],
)
def test_invalid_policy_evaluation_identifier_is_rejected(
    raw_value: str,
) -> None:
    with pytest.raises(PolicyEvaluationError):
        PolicyEvaluationId.parse(raw_value)