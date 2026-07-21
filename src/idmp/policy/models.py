from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from idmp.core import PolicyError
from idmp.policy.identifiers import PolicyId, PolicyType


class PolicyStatus(StrEnum):
    """Represents the lifecycle status of a Policy."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"


@dataclass(frozen=True, slots=True)
class Policy:
    """
    Defines a reusable rule that governs proposed Decisions.

    A Policy describes a rule but does not evaluate a Decision,
    authorize an action, or execute external behavior.
    """

    policy_id: PolicyId
    policy_type: PolicyType
    created_at: datetime
    name: str
    description: str
    version: str
    status: PolicyStatus = PolicyStatus.ACTIVE

    def __post_init__(self) -> None:
        self._validate_identifier_type()
        self._validate_created_at()
        self._normalize_text_fields()
        self._validate_status()

    def _validate_identifier_type(self) -> None:
        if self.policy_id.policy_type != self.policy_type:
            raise PolicyError(
                "Policy ID type must match the Policy type"
            )

    def _validate_created_at(self) -> None:
        if (
            self.created_at.tzinfo is None
            or self.created_at.utcoffset() is None
        ):
            raise PolicyError(
                "created_at must be timezone-aware"
            )

    def _normalize_text_fields(self) -> None:
        normalized_name = self.name.strip()
        normalized_description = self.description.strip()
        normalized_version = self.version.strip()

        if not normalized_name:
            raise PolicyError("name must not be empty")

        if not normalized_description:
            raise PolicyError("description must not be empty")

        if not normalized_version:
            raise PolicyError("version must not be empty")

        object.__setattr__(self, "name", normalized_name)
        object.__setattr__(
            self,
            "description",
            normalized_description,
        )
        object.__setattr__(self, "version", normalized_version)

    def _validate_status(self) -> None:
        if not isinstance(self.status, PolicyStatus):
            raise PolicyError(
                "status must be a valid PolicyStatus"
            )