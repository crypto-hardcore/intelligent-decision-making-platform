import pytest

from idmp.core.exceptions import (
    ConfigurationError,
    ConnectorError,
    GovernanceError,
    ObservationError,
    PlanningError,
    PlatformError,
    ValidationError,
)


@pytest.mark.parametrize(
    "exception_type",
    [
        ValidationError,
        ConfigurationError,
        ObservationError,
        PlanningError,
        GovernanceError,
        ConnectorError,
    ],
)
def test_platform_exceptions_inherit_from_platform_error(
    exception_type: type[PlatformError],
) -> None:
    assert issubclass(exception_type, PlatformError)


def test_platform_error_inherits_from_exception() -> None:
    assert issubclass(PlatformError, Exception)


def test_platform_error_preserves_message() -> None:
    error = PlatformError("Something went wrong")

    assert str(error) == "Something went wrong"