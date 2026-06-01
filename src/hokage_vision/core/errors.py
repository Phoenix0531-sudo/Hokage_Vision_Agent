class HokageVisionError(Exception):
    """Base exception for Hokage Vision Agent."""


class ConfigError(HokageVisionError):
    """Raised when configuration loading or validation fails."""


class VisionBackendError(HokageVisionError):
    """Raised when a vision backend cannot load or predict."""


class DatasetValidationError(HokageVisionError):
    """Raised when dataset validation cannot complete."""
