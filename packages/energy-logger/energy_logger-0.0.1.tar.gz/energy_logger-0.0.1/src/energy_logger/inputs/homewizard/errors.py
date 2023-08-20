from enum import IntEnum

from pydantic import BaseModel


class ErrorCodeEnum(IntEnum):
    BodyContainsInvalidJSON = 2
    InvalidValueForParameter = 7
    ParameterIsNotModifiable = 8
    RequestTooLong = 201
    APIDisabled = 202
    InternalError = 901


class HomeWizardError(BaseModel):
    id: ErrorCodeEnum  # noqa
    description: str


class HomeWizardErrorResponse(BaseModel):
    error: HomeWizardError

    def __str__(self) -> str:
        return f"Error code {self.error.id}: {self.error.description}"
