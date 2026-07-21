"""
Core exception hierarchy for the Intelligent Decision-Making Platform.

All platform-specific exceptions should inherit from PlatformError.
"""


class PlatformError(Exception):
    """Base class for all platform-specific exceptions."""


class ValidationError(PlatformError):
    """Raised when domain validation fails."""


class ConfigurationError(PlatformError):
    """Raised when platform configuration is invalid."""


class ObservationError(PlatformError):
    """Raised when an Observation is invalid or inconsistent."""


class EvidenceError(PlatformError):
    """Raised when Evidence is invalid or inconsistent."""


class PlanningError(PlatformError):
    """Raised when an Execution Plan cannot be created safely."""


class GovernanceError(PlatformError):
    """Raised when governance evaluation or authorization fails."""


class ConnectorError(PlatformError):
    """Raised when communication with an external system fails."""


