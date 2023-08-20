import logging
import tomllib
from os import PathLike
from typing import Any

from pydantic import ValidationError
from pydantic_settings import BaseSettings

from energy_logger.inputs.homewizard.p1.settings import HomeWizardP1Settings

logger = logging.getLogger(__name__)


class InputSettings(BaseSettings):
    homewizard_p1: HomeWizardP1Settings | None = None


class Settings(BaseSettings):
    inputs: InputSettings


def get_settings(file: PathLike | str | None = None, data: dict[str, Any] | str | None = None) -> Settings | None:
    """
    Read and validate the settings from either a settings file, toml string or dict
    """

    if data is None:
        if file is None:
            return None  # TODO: search for config in sensible default locations

        with open(file, "rb") as f:
            _data = tomllib.load(f)
    elif isinstance(data, dict):
        _data = data
    else:
        _data = tomllib.loads(data)

    try:
        settings = Settings(**_data)
    except ValidationError as exc:
        logging.error(exc)
        return None

    return settings
