"""Stable identity types for Observation artifacts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from idmp.core import ObservationError

_TYPE_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True, slots=True)
class ObservationType:
    """Validated, extensible classification of an Observation."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not normalized:
            raise ObservationError("Observation type must not be empty.")
        if _TYPE_PATTERN.fullmatch(normalized) is None:
            raise ObservationError(
                "Observation type must start with a letter and contain only "
                "lowercase letters, numbers, or hyphens."
            )
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ObservationId:
    """Globally unique identity for an Observation artifact."""

    observation_type: ObservationType
    unique_id: UUID

    @classmethod
    def create(cls, observation_type: ObservationType) -> ObservationId:
        return cls(observation_type=observation_type, unique_id=uuid4())

    @classmethod
    def parse(cls, raw_value: str) -> ObservationId:
        parts = raw_value.strip().split("_", maxsplit=2)
        if len(parts) != 3 or parts[0] != "obs":
            raise ObservationError(
                "Observation ID must use the form obs_<observation-type>_<uuid>."
            )

        try:
            observation_type = ObservationType(parts[1])
            unique_id = UUID(parts[2])
        except ValueError as error:
            raise ObservationError("Observation ID contains an invalid UUID.") from error

        return cls(observation_type=observation_type, unique_id=unique_id)

    def __str__(self) -> str:
        return f"obs_{self.observation_type}_{self.unique_id}"
