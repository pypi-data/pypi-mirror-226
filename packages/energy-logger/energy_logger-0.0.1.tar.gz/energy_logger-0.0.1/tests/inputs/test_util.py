import pytest

from energy_logger.inputs.homewizard.p1.settings import HomeWizardP1Settings
from energy_logger.inputs.util import get_active_inputs
from energy_logger.settings import Settings, InputSettings


def test_get_active_inputs():
    settings = Settings(
        inputs=InputSettings(homewizard_p1=HomeWizardP1Settings(
            ipaddress='127.0.0.1'
        ))
    )

    active_inputs = get_active_inputs(settings)

    assert 'homewizard_p1' in active_inputs


def test_get_active_inputs_no_settings():
    settings = Settings(inputs=InputSettings())

    with pytest.raises(ValueError) as exc_info:
        get_active_inputs(settings)

    assert (
            "At least one input should be defined in the settings file"
            == str(exc_info.value)
    )


