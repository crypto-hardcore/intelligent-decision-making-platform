from __future__ import annotations

import pytest

from idmp.core import EvidenceError
from idmp.evidence import EvidenceId, EvidenceType


def test_evidence_type_is_normalized() -> None:
    evidence_type = EvidenceType(" Technical-Analysis ")

    assert evidence_type.value == "technical-analysis"


def test_evidence_type_must_not_be_empty() -> None:
    with pytest.raises(EvidenceError):
        EvidenceType("   ")


@pytest.mark.parametrize(
    "value",
    [
        "123analysis",
        "technical_analysis",
        "technical analysis",
        "technical!",
    ],
)
def test_invalid_evidence_type_is_rejected(value: str) -> None:
    with pytest.raises(EvidenceError):
        EvidenceType(value)


def test_create_evidence_id() -> None:
    evidence_type = EvidenceType("technical-analysis")

    evidence_id = EvidenceId.create(evidence_type)

    assert evidence_id.evidence_type == evidence_type


def test_parse_round_trip() -> None:
    original = EvidenceId.create(EvidenceType("market"))

    parsed = EvidenceId.parse(str(original))

    assert parsed == original


@pytest.mark.parametrize(
    "raw_value",
    [
        "",
        "abc",
        "evd_market",
        "evd_market_not-a-uuid",
        "obs_market_123",
    ],
)
def test_invalid_identifier_is_rejected(raw_value: str) -> None:
    with pytest.raises(EvidenceError):
        EvidenceId.parse(raw_value)