from __future__ import annotations

import pytest

from idmp.core import DecisionError
from idmp.decision import DecisionId, DecisionType


def test_decision_type_is_normalized() -> None:
    decision_type = DecisionType(" Enter-Position ")

    assert decision_type.value == "enter-position"


def test_decision_type_string_representation() -> None:
    decision_type = DecisionType("enter-position")

    assert str(decision_type) == "enter-position"


def test_decision_type_must_not_be_empty() -> None:
    with pytest.raises(
        DecisionError,
        match="Decision type must not be empty",
    ):
        DecisionType("   ")


@pytest.mark.parametrize(
    "value",
    [
        "123decision",
        "enter_position",
        "enter position",
        "enter!",
        "-enter-position",
    ],
)
def test_invalid_decision_type_is_rejected(value: str) -> None:
    with pytest.raises(DecisionError):
        DecisionType(value)


def test_create_decision_id() -> None:
    decision_type = DecisionType("enter-position")

    decision_id = DecisionId.create(decision_type)

    assert decision_id.decision_type == decision_type


def test_decision_id_string_representation() -> None:
    decision_type = DecisionType("enter-position")
    decision_id = DecisionId.create(decision_type)

    assert str(decision_id) == (
        f"dec_enter-position_{decision_id.value}"
    )


def test_parse_decision_id_round_trip() -> None:
    original = DecisionId.create(
        DecisionType("enter-position")
    )

    parsed = DecisionId.parse(str(original))

    assert parsed == original


def test_parse_preserves_decision_type() -> None:
    original = DecisionId.create(
        DecisionType("reduce-exposure")
    )

    parsed = DecisionId.parse(str(original))

    assert parsed.decision_type == DecisionType("reduce-exposure")


@pytest.mark.parametrize(
    "raw_value",
    [
        "",
        "abc",
        "dec_enter-position",
        "dec__123",
        "dec_enter-position_not-a-uuid",
        "asm_enter-position_123",
        "dec_123decision_00000000-0000-0000-0000-000000000000",
    ],
)
def test_invalid_decision_identifier_is_rejected(
    raw_value: str,
) -> None:
    with pytest.raises(DecisionError):
        DecisionId.parse(raw_value)