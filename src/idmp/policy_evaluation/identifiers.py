from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID, uuid4

from idmp.core import PolicyEvaluationError


_POLICY_EVALUATION_TYPE_PATTERN = re.compile(
    r"^[a-z][a-z0-9-]*$"
)


@dataclass(frozen=True, slots=True)
class PolicyEvaluationType:
    value: str

    def __post_init__(self) -> None:
        normalized_value = self.value.strip().lower()

        if not normalized_value:
            raise PolicyEvaluationError(
                "Policy evaluation type must not be empty"
            )

        if not _POLICY_EVALUATION_TYPE_PATTERN.fullmatch(
            normalized_value
        ):
            raise PolicyEvaluationError(
                "Policy evaluation type contains invalid characters"
            )

        object.__setattr__(self, "value", normalized_value)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class PolicyEvaluationId:
    policy_evaluation_type: PolicyEvaluationType
    value: UUID

    @classmethod
    def create(
        cls,
        policy_evaluation_type: PolicyEvaluationType,
    ) -> PolicyEvaluationId:
        return cls(
            policy_evaluation_type=policy_evaluation_type,
            value=uuid4(),
        )

    @classmethod
    def parse(cls, raw_value: str) -> PolicyEvaluationId:
        try:
            prefix, type_value, uuid_value = raw_value.split(
                "_",
                maxsplit=2,
            )
        except ValueError as error:
            raise PolicyEvaluationError(
                "Invalid PolicyEvaluation identifier format"
            ) from error

        if prefix != "peval":
            raise PolicyEvaluationError(
                "Invalid PolicyEvaluation identifier prefix"
            )

        try:
            policy_evaluation_type = PolicyEvaluationType(
                type_value
            )
            identifier_value = UUID(uuid_value)
        except (PolicyEvaluationError, ValueError) as error:
            raise PolicyEvaluationError(
                "Invalid PolicyEvaluation identifier"
            ) from error

        return cls(
            policy_evaluation_type=policy_evaluation_type,
            value=identifier_value,
        )

    def __str__(self) -> str:
        return (
            f"peval_{self.policy_evaluation_type}_{self.value}"
        )