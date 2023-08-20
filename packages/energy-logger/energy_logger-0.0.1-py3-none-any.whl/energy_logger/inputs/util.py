from energy_logger.inputs.homewizard import HomeWizardP1Input
from energy_logger.inputs.protocols import InputProtocol
from energy_logger.settings import Settings

ALL_INPUTS: dict[str, InputProtocol] = {
    "homewizard_p1": HomeWizardP1Input
}


def get_active_inputs(settings: Settings) -> dict[str, InputProtocol]:
    """
    Gets all active (in settings) inputs as a dict of inputs.
    Inputs will be initialised with their respective settings
    """
    active_inputs: dict[str, InputProtocol] = {}

    if (homewizard_p1_settings := settings.inputs.homewizard_p1) is not None:
        active_inputs["homewizard_p1"] = HomeWizardP1Input(homewizard_p1_settings)

    if not active_inputs:
        msg = "At least one input should be defined in the settings file"
        raise ValueError(msg)

    return active_inputs
