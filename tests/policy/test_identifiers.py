from __future__ import annotations

import pytest

from idmp.core import PolicyError
from idmp.policy import PolicyId, PolicyType


def test_policy_type_is_normalized() -> None:
    policy_type = PolicyType(" Maximum-Risk ")

    assert policy_type.value == "maximum-risk"


def test_policy_type_string_representation() -> None:
    policy_type = PolicyType("maximum-risk")

    assert str(policy_type) == "maximum-risk"


def test_policy_type_must_not_be_empty() -> None:
    with pytest.raises(
        PolicyError,
        match="Policy type must not be empty",
    ):
        PolicyType("   ")


@pytest.mark.parametrize(
    "value",
    [
        "123policy",
        "maximum_risk",
        "maximum risk",
        "maximum!",
        "-maximum-risk",
    ],
)
def test_invalid_policy_type_is_rejected(value: str) -> None:
    with pytest.raises(PolicyError):
        PolicyType(value)


def test_create_policy_id() -> None:
    policy_type = PolicyType("maximum-risk")

    policy_id = PolicyId.create(policy_type)

    assert policy_id.policy_type == policy_type


def test_policy_id_string_representation() -> None:
    policy_type = PolicyType("maximum-risk")
    policy_id = PolicyId.create(policy_type)

    assert str(policy_id) == (
        f"pol_maximum-risk_{policy_id.value}"
    )


def test_parse_policy_id_round_trip() -> None:
    original = PolicyId.create(
        PolicyType("maximum-risk")
    )

    parsed = PolicyId.parse(str(original))

    assert parsed == original


def test_parse_preserves_policy_type() -> None:
    original = PolicyId.create(
        PolicyType("daily-loss-limit")
    )

    parsed = PolicyId.parse(str(original))

    assert parsed.policy_type == PolicyType(
        "daily-loss-limit"
    )


@pytest.mark.parametrize(
    "raw_value",
    [
        "",
        "abc",
        "pol_maximum-risk",
        "pol__123",
        "pol_maximum-risk_not-a-uuid",
        "dec_maximum-risk_00000000-0000-0000-0000-000000000000",
        "pol_123policy_00000000-0000-0000-0000-000000000000",
    ],
)
def test_invalid_policy_identifier_is_rejected(
    raw_value: str,
) -> None:
    with pytest.raises(PolicyError):
        PolicyId.parse(raw_value)