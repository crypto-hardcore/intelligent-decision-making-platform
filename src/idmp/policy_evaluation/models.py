from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from idmp.core import PolicyEvaluationError
from idmp.decision import Decision
from idmp.policy import Policy
from idmp.policy_evaluation.identifiers import (
    PolicyEvaluationId,
    PolicyEvaluationType,
)


class PolicyEvaluationResult(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    NOT_APPLICABLE = "not-applicable"


@dataclass(frozen=True, slots=True)
class PolicyEvaluation:
    policy_evaluation_id: PolicyEvaluationId
    policy_evaluation_type: PolicyEvaluationType
    evaluated_at: datetime
    decision: Decision
    policy: Policy
    result: PolicyEvaluationResult
    explanation: str
    violations: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        self._validate_identifier()
        self._validate_evaluated_at()
        self._validate_references()
        self._validate_result()

        normalized_explanation = self._normalize_required_text(
            self.explanation,
            field_name="explanation",
        )
        normalized_violations = self._normalize_messages(
            self.violations,
            field_name="violations",
        )
        normalized_warnings = self._normalize_messages(
            self.warnings,
            field_name="warnings",
        )

        self._validate_result_consistency(
            normalized_violations,
        )

        object.__setattr__(
            self,
            "explanation",
            normalized_explanation,
        )
        object.__setattr__(
            self,
            "violations",
            normalized_violations,
        )
        object.__setattr__(
            self,
            "warnings",
            normalized_warnings,
        )

    def _validate_identifier(self) -> None:
        if not isinstance(
            self.policy_evaluation_id,
            PolicyEvaluationId,
        ):
            raise PolicyEvaluationError(
                "policy_evaluation_id must be a "
                "PolicyEvaluationId"
            )

        if not isinstance(
            self.policy_evaluation_type,
            PolicyEvaluationType,
        ):
            raise PolicyEvaluationError(
                "policy_evaluation_type must be a "
                "PolicyEvaluationType"
            )

        if (
            self.policy_evaluation_id.policy_evaluation_type
            != self.policy_evaluation_type
        ):
            raise PolicyEvaluationError(
                "PolicyEvaluation ID type must match the "
                "PolicyEvaluation type"
            )

    def _validate_evaluated_at(self) -> None:
        if not isinstance(self.evaluated_at, datetime):
            raise PolicyEvaluationError(
                "evaluated_at must be a datetime"
            )

        if (
            self.evaluated_at.tzinfo is None
            or self.evaluated_at.utcoffset() is None
        ):
            raise PolicyEvaluationError(
                "evaluated_at must be timezone-aware"
            )

    def _validate_references(self) -> None:
        if not isinstance(self.decision, Decision):
            raise PolicyEvaluationError(
                "decision must be a Decision"
            )

        if not isinstance(self.policy, Policy):
            raise PolicyEvaluationError(
                "policy must be a Policy"
            )

    def _validate_result(self) -> None:
        if not isinstance(
            self.result,
            PolicyEvaluationResult,
        ):
            raise PolicyEvaluationError(
                "result must be a valid "
                "PolicyEvaluationResult"
            )

    def _validate_result_consistency(
        self,
        violations: tuple[str, ...],
    ) -> None:
        if (
            self.result is PolicyEvaluationResult.FAILED
            and not violations
        ):
            raise PolicyEvaluationError(
                "A failed PolicyEvaluation must contain "
                "at least one violation"
            )

        if (
            self.result
            in {
                PolicyEvaluationResult.PASSED,
                PolicyEvaluationResult.NOT_APPLICABLE,
            }
            and violations
        ):
            raise PolicyEvaluationError(
                "Only a failed PolicyEvaluation may contain "
                "violations"
            )

    @staticmethod
    def _normalize_required_text(
        value: str,
        *,
        field_name: str,
    ) -> str:
        if not isinstance(value, str):
            raise PolicyEvaluationError(
                f"{field_name} must be a string"
            )

        normalized_value = value.strip()

        if not normalized_value:
            raise PolicyEvaluationError(
                f"{field_name} must not be empty"
            )

        return normalized_value

    @classmethod
    def _normalize_messages(
        cls,
        values: tuple[str, ...],
        *,
        field_name: str,
    ) -> tuple[str, ...]:
        if not isinstance(values, tuple):
            raise PolicyEvaluationError(
                f"{field_name} must be a tuple"
            )

        normalized_values = tuple(
            cls._normalize_required_text(
                value,
                field_name=f"{field_name} entry",
            )
            for value in values
        )

        if len(normalized_values) != len(
            set(normalized_values)
        ):
            raise PolicyEvaluationError(
                f"{field_name} must not contain duplicates"
            )

        return normalized_values