from __future__ import annotations

import pytest

from idmp.assessment import AssessmentId, AssessmentType
from idmp.core import AssessmentError


def test_assessment_type_is_normalized() -> None:
    assessment_type = AssessmentType(" Market-Bias ")

    assert assessment_type.value == "market-bias"


def test_assessment_type_must_not_be_empty() -> None:
    with pytest.raises(AssessmentError):
        AssessmentType("   ")


@pytest.mark.parametrize(
    "value",
    [
        "123market",
        "market_bias",
        "market bias",
        "market!",
    ],
)
def test_invalid_assessment_type_is_rejected(value: str) -> None:
    with pytest.raises(AssessmentError):
        AssessmentType(value)


def test_create_assessment_id() -> None:
    assessment_type = AssessmentType("market-bias")

    assessment_id = AssessmentId.create(assessment_type)

    assert assessment_id.assessment_type == assessment_type


def test_parse_round_trip() -> None:
    original = AssessmentId.create(
        AssessmentType("market-bias")
    )

    parsed = AssessmentId.parse(str(original))

    assert parsed == original


@pytest.mark.parametrize(
    "raw_value",
    [
        "",
        "abc",
        "asm_market",
        "asm_market_not-a-uuid",
        "obs_market_123",
    ],
)
def test_invalid_identifier_is_rejected(raw_value: str) -> None:
    with pytest.raises(AssessmentError):
        AssessmentId.parse(raw_value)