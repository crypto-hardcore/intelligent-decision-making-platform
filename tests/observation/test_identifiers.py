from uuid import UUID

import pytest

from idmp.core import ObservationError
from idmp.observation import ObservationId, ObservationType


def test_observation_type_is_normalized() -> None:
    assert ObservationType(" Price ").value == "price"


@pytest.mark.parametrize("raw_value", ["", "1price", "price data", "PRICE!"])
def test_invalid_observation_type_is_rejected(raw_value: str) -> None:
    with pytest.raises(ObservationError):
        ObservationType(raw_value)


def test_observation_id_uses_canonical_form() -> None:
    observation_id = ObservationId(
        observation_type=ObservationType("price"),
        unique_id=UUID("12345678-1234-5678-1234-567812345678"),
    )

    assert str(observation_id) == (
        "obs_price_12345678-1234-5678-1234-567812345678"
    )


def test_observation_id_round_trip() -> None:
    raw_value = "obs_price_12345678-1234-5678-1234-567812345678"

    assert str(ObservationId.parse(raw_value)) == raw_value


@pytest.mark.parametrize(
    "raw_value",
    [
        "",
        "price_12345678-1234-5678-1234-567812345678",
        "obs_price_not-a-uuid",
    ],
)
def test_invalid_observation_id_is_rejected(raw_value: str) -> None:
    with pytest.raises(ObservationError):
        ObservationId.parse(raw_value)
