from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta

import pytest

from idmp.core import ObservationError
from idmp.observation import (
    DataQuality,
    Observation,
    ObservationId,
    ObservationType,
    Provenance,
)


def make_observation(**overrides: object) -> Observation:
    observation_type = ObservationType("price")
    values: dict[str, object] = {
        "observation_id": ObservationId.create(observation_type),
        "observation_type": observation_type,
        "observed_at": datetime(2026, 7, 21, 10, 0, tzinfo=UTC),
        "recorded_at": datetime(2026, 7, 21, 10, 0, 1, tzinfo=UTC),
        "subject": "BTCUSDT",
        "value": {"price": 118000.0},
        "unit": "USDT",
        "provenance": Provenance(
            source="Binance Futures",
            collection_method="REST API",
            collector="binance-connector",
            source_record_id="trade-123",
        ),
        "data_quality": DataQuality(is_complete=True),
    }
    values.update(overrides)
    return Observation(**values)  # type: ignore[arg-type]


def test_valid_observation_is_created() -> None:
    observation = make_observation()

    assert observation.subject == "BTCUSDT"
    assert observation.unit == "USDT"


def test_observation_is_immutable() -> None:
    observation = make_observation()

    with pytest.raises(FrozenInstanceError):
        observation.subject = "ETHUSDT"  # type: ignore[misc]


def test_observation_value_is_deeply_immutable() -> None:
    observation = make_observation(value={"levels": [1, 2, 3]})

    assert observation.value["levels"] == (1, 2, 3)  # type: ignore[index]
    with pytest.raises(TypeError):
        observation.value["levels"] = (4,)  # type: ignore[index]


def test_observation_id_type_must_match_observation_type() -> None:
    price_type = ObservationType("price")
    news_type = ObservationType("news")

    with pytest.raises(ObservationError, match="must match"):
        make_observation(
            observation_id=ObservationId.create(price_type),
            observation_type=news_type,
        )


@pytest.mark.parametrize("field_name", ["observed_at", "recorded_at"])
def test_observation_timestamps_must_be_timezone_aware(field_name: str) -> None:
    with pytest.raises(ObservationError, match="timezone-aware"):
        make_observation(**{field_name: datetime(2026, 7, 21, 10, 0)})


def test_recorded_at_must_not_precede_observed_at() -> None:
    observed_at = datetime(2026, 7, 21, 10, 0, tzinfo=UTC)

    with pytest.raises(ObservationError, match="must not be earlier"):
        make_observation(
            observed_at=observed_at,
            recorded_at=observed_at - timedelta(seconds=1),
        )


@pytest.mark.parametrize("field_name", ["subject", "unit"])
def test_blank_observation_text_is_rejected(field_name: str) -> None:
    with pytest.raises(ObservationError):
        make_observation(**{field_name: "   "})


def test_complete_data_quality_cannot_contain_issues() -> None:
    with pytest.raises(ObservationError, match="cannot contain"):
        DataQuality(is_complete=True, issues=("Delayed source",))


def test_incomplete_data_quality_preserves_issues() -> None:
    quality = DataQuality(is_complete=False, issues=("Delayed source",))

    assert quality.issues == ("Delayed source",)


def test_observation_does_not_expose_recommendation_field() -> None:
    assert "recommendation" not in Observation.__dataclass_fields__
