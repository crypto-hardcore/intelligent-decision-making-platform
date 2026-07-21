"""Canonical Observation domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Mapping, TypeAlias

from idmp.core import ObservationError
from idmp.observation.identifiers import ObservationId, ObservationType

ObservationScalar: TypeAlias = str | int | float | bool | None
ObservationValue: TypeAlias = (
    ObservationScalar
    | tuple["ObservationValue", ...]
    | Mapping[str, "ObservationValue"]
)


def _require_text(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ObservationError(f"{field_name} must not be empty.")
    return normalized


def _require_aware_datetime(value: datetime, field_name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ObservationError(f"{field_name} must be timezone-aware.")


def _freeze_value(value: ObservationValue) -> ObservationValue:
    if isinstance(value, Mapping):
        frozen = {str(key): _freeze_value(item) for key, item in value.items()}
        return MappingProxyType(frozen)
    if isinstance(value, tuple):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise ObservationError(
        "Observation value must contain only JSON-compatible scalar, sequence, "
        "or mapping values."
    )


@dataclass(frozen=True, slots=True)
class Provenance:
    """Origin and collection details for an Observation."""

    source: str
    collection_method: str
    collector: str
    source_record_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "source", _require_text(self.source, "source"))
        object.__setattr__(
            self,
            "collection_method",
            _require_text(self.collection_method, "collection_method"),
        )
        object.__setattr__(
            self, "collector", _require_text(self.collector, "collector")
        )
        if self.source_record_id is not None:
            object.__setattr__(
                self,
                "source_record_id",
                _require_text(self.source_record_id, "source_record_id"),
            )


@dataclass(frozen=True, slots=True)
class DataQuality:
    """Factual data-quality information attached to an Observation."""

    is_complete: bool
    issues: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        normalized_issues = tuple(
            _require_text(issue, "data-quality issue") for issue in self.issues
        )
        if self.is_complete and normalized_issues:
            raise ObservationError(
                "A complete Observation cannot contain data-quality issues."
            )
        object.__setattr__(self, "issues", normalized_issues)


@dataclass(frozen=True, slots=True)
class Observation:
    """Immutable factual representation of something observed or recorded."""

    observation_id: ObservationId
    observation_type: ObservationType
    observed_at: datetime
    recorded_at: datetime
    subject: str
    value: ObservationValue
    provenance: Provenance
    data_quality: DataQuality
    unit: str | None = None

    def __post_init__(self) -> None:
        if self.observation_id.observation_type != self.observation_type:
            raise ObservationError(
                "Observation ID type must match the Observation type."
            )

        _require_aware_datetime(self.observed_at, "observed_at")
        _require_aware_datetime(self.recorded_at, "recorded_at")
        if self.recorded_at < self.observed_at:
            raise ObservationError(
                "recorded_at must not be earlier than observed_at."
            )

        object.__setattr__(self, "subject", _require_text(self.subject, "subject"))
        object.__setattr__(self, "value", _freeze_value(self.value))

        if self.unit is not None:
            object.__setattr__(self, "unit", _require_text(self.unit, "unit"))
