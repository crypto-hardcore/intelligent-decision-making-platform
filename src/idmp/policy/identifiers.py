from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from idmp.core import PolicyError

_POLICY_TYPE_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True, slots=True)
class PolicyType:
    """Represents the type of a Policy."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise PolicyError("Policy type must not be empty")

        if not _POLICY_TYPE_PATTERN.fullmatch(normalized):
            raise PolicyError(
                "Policy type must start with a letter and contain only "
                "lowercase letters, digits, and hyphens"
            )

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class PolicyId:
    """Unique identifier for a Policy."""

    policy_type: PolicyType
    value: UUID

    @classmethod
    def create(cls, policy_type: PolicyType) -> "PolicyId":
        """Create a new Policy identifier."""
        return cls(
            policy_type=policy_type,
            value=uuid4(),
        )

    @classmethod
    def parse(cls, raw_value: str) -> "PolicyId":
        """
        Parse a serialized Policy identifier.

        Expected format:

            pol_<policy-type>_<uuid>
        """
        try:
            prefix, policy_type, uuid_text = raw_value.split("_", maxsplit=2)
        except ValueError as error:
            raise PolicyError("Invalid Policy identifier") from error

        if prefix != "pol":
            raise PolicyError("Invalid Policy identifier")

        try:
            return cls(
                policy_type=PolicyType(policy_type),
                value=UUID(uuid_text),
            )
        except (ValueError, PolicyError) as error:
            raise PolicyError("Invalid Policy identifier") from error

    def __str__(self) -> str:
        return f"pol_{self.policy_type}_{self.value}"