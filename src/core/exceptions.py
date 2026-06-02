"""Custom exceptions for the application."""


class PipelineException(Exception):
    """Base exception for pipeline errors."""
    pass


class DataValidationError(PipelineException):
    """Raised when input data validation fails."""
    pass


class ModelNotFoundError(PipelineException):
    """Raised when model file is not found."""
    pass


class PredictionError(PipelineException):
    """Raised when prediction fails."""
    pass


class FeatureEngineeringError(PipelineException):
    """Raised when feature engineering fails."""
    pass
