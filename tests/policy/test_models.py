from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from idmp.core import PolicyError
from idmp.policy import (
    Policy,
    PolicyId,
    PolicyStatus,
    PolicyType,
)


def make_policy(
    *,
    policy_type: PolicyType | None = None,
    policy_id: PolicyId | None = None,
    created_at: datetime | None = None,
    name: str = "Maximum Risk Policy",
    description: str = (
        "Limits the maximum risk allowed for a proposed decision."
    ),
    version: str = "1.0",
    status: PolicyStatus = PolicyStatus.ACTIVE,
) -> Policy:
    resolved_type = policy_type or PolicyType("maximum-risk")
    resolved_id = policy_id or PolicyId.create(resolved_type)

    return Policy(
        policy_id=resolved_id,
        policy_type=resolved_type,
        created_at=created_at
        or datetime(2026, 7, 21, 11, 0, tzinfo=UTC),
        name=name,
        description=description,
        version=version,
        status=status,
    )


def test_valid_policy_is_created() -> None:
    policy = make_policy()

    assert policy.policy_type == PolicyType("maximum-risk")
    assert policy.status is PolicyStatus.ACTIVE


def test_name_is_normalized() -> None:
    policy = make_policy(
        name="  Maximum Risk Policy  ",
    )

    assert policy.name == "Maximum Risk Policy"


def test_description_is_normalized() -> None:
    policy = make_policy(
        description="  Risk must remain below 1%.  ",
    )

    assert policy.description == "Risk must remain below 1%."


def test_version_is_normalized() -> None:
    policy = make_policy(
        version="  1.0  ",
    )

    assert policy.version == "1.0"


def test_policy_id_type_must_match_policy_type() -> None:
    identifier_type = PolicyType("maximum-risk")
    policy_id = PolicyId.create(identifier_type)

    with pytest.raises(
        PolicyError,
        match="Policy ID type must match the Policy type",
    ):
        make_policy(
            policy_type=PolicyType("daily-loss-limit"),
            policy_id=policy_id,
        )


def test_created_at_must_be_timezone_aware() -> None:
    with pytest.raises(
        PolicyError,
        match="created_at must be timezone-aware",
    ):
        make_policy(
            created_at=datetime(2026, 7, 21, 11, 0),
        )


def test_empty_name_is_rejected() -> None:
    with pytest.raises(
        PolicyError,
        match="name must not be empty",
    ):
        make_policy(name="   ")


def test_empty_description_is_rejected() -> None:
    with pytest.raises(
        PolicyError,
        match="description must not be empty",
    ):
        make_policy(description="   ")


def test_empty_version_is_rejected() -> None:
    with pytest.raises(
        PolicyError,
        match="version must not be empty",
    ):
        make_policy(version="   ")


def test_status_must_be_valid_policy_status() -> None:
    with pytest.raises(
        PolicyError,
        match="status must be a valid PolicyStatus",
    ):
        make_policy(
            status="active",  # type: ignore[arg-type]
        )


def test_deprecated_policy_is_allowed() -> None:
    policy = make_policy(
        status=PolicyStatus.DEPRECATED,
    )

    assert policy.status is PolicyStatus.DEPRECATED


def test_policy_is_immutable() -> None:
    policy = make_policy()

    with pytest.raises(FrozenInstanceError):
        policy.name = "Modified"  # type: ignore[misc]