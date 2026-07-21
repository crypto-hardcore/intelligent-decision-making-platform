from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from idmp.core import EvidenceError
from idmp.evidence import Evidence, EvidenceId, EvidenceType
from idmp.observation import (
    DataQuality,
    Observation,
    ObservationId,
    ObservationType,
    Provenance,
)


def make_observation() -> Observation:
    observation_type = ObservationType("market-price")

    return Observation(
        observation_id=ObservationId.create(observation_type),
        observation_type=observation_type,
        observed_at=datetime(2026, 7, 21, 8, 0, tzinfo=timezone.utc),
        recorded_at=datetime(2026, 7, 21, 8, 1, tzinfo=timezone.utc),
        subject="BTCUSDT",
        value=118_500.0,
        provenance=Provenance(
            source="Binance",
            collection_method="REST API",
            collector="IDMP market-data adapter",
            source_record_id="btc-price-20260721-0800",
        ),
        data_quality=DataQuality(is_complete=True),
        unit="USDT",
    )


def make_evidence(
    *,
    evidence_type: EvidenceType | None = None,
    evidence_id: EvidenceId | None = None,
    created_at: datetime | None = None,
    statement: str = "BTCUSDT was recorded at 118,500 USDT.",
    observations: tuple[Observation, ...] | None = None,
) -> Evidence:
    resolved_type = evidence_type or EvidenceType("market-context")
    resolved_id = evidence_id or EvidenceId.create(resolved_type)

    return Evidence(
        evidence_id=resolved_id,
        evidence_type=resolved_type,
        created_at=created_at
        or datetime(2026, 7, 21, 8, 2, tzinfo=timezone.utc),
        statement=statement,
        observations=observations or (make_observation(),),
    )


def test_create_valid_evidence() -> None:
    evidence = make_evidence()

    assert evidence.evidence_type == EvidenceType("market-context")
    assert evidence.statement == "BTCUSDT was recorded at 118,500 USDT."
    assert len(evidence.observations) == 1


def test_statement_is_normalized() -> None:
    evidence = make_evidence(
        statement="  BTCUSDT was recorded at 118,500 USDT.  "
    )

    assert evidence.statement == "BTCUSDT was recorded at 118,500 USDT."


def test_empty_statement_is_rejected() -> None:
    with pytest.raises(EvidenceError, match="statement must not be empty"):
        make_evidence(statement="   ")


def test_created_at_must_be_timezone_aware() -> None:
    naive_datetime = datetime(2026, 7, 21, 8, 2)

    with pytest.raises(
        EvidenceError,
        match="created_at must be timezone-aware",
    ):
        make_evidence(created_at=naive_datetime)


def test_evidence_id_type_must_match_evidence_type() -> None:
    identifier_type = EvidenceType("market-context")
    evidence_id = EvidenceId.create(identifier_type)

    with pytest.raises(
        EvidenceError,
        match="Evidence ID type must match the Evidence type",
    ):
        make_evidence(
            evidence_type=EvidenceType("operational-context"),
            evidence_id=evidence_id,
        )


def test_evidence_requires_at_least_one_observation() -> None:
    evidence_type = EvidenceType("market-context")

    with pytest.raises(
        EvidenceError,
        match="Evidence must reference at least one Observation",
    ):
        Evidence(
            evidence_id=EvidenceId.create(evidence_type),
            evidence_type=evidence_type,
            created_at=datetime(
                2026,
                7,
                21,
                8,
                2,
                tzinfo=timezone.utc,
            ),
            statement="No supporting observations exist.",
            observations=(),
        )


def test_evidence_preserves_supporting_observations() -> None:
    first_observation = make_observation()
    second_observation = make_observation()

    evidence = make_evidence(
        observations=(first_observation, second_observation)
    )

    assert evidence.observations == (
        first_observation,
        second_observation,
    )


def test_evidence_is_immutable() -> None:
    evidence = make_evidence()

    with pytest.raises(FrozenInstanceError):
        evidence.statement = "Modified statement."  # type: ignore[misc]