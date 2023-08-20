import logging

import httpx
from pydantic import ValidationError, IPvAnyAddress

from energy_logger.inputs.homewizard.errors import HomeWizardErrorResponse
from energy_logger.inputs.homewizard.p1.response import HomeWizardP1Response
from energy_logger.inputs.homewizard.p1.settings import HomeWizardP1Settings
from energy_logger.inputs.protocols import InputProtocol
from energy_logger.models import P1Data

logger = logging.getLogger(__name__)


class HomeWizardP1Input(InputProtocol):
    settings: HomeWizardP1Settings

    def __init__(self, settings: HomeWizardP1Settings) -> None:
        self.settings = settings

    @property
    def ipaddress(self) -> IPvAnyAddress:
        return self.settings.ipaddress

    @property
    def api_url(self) -> str:
        return f"http://{self.ipaddress}/api/v1/data/"

    async def read_data(self) -> P1Data | None:
        """
        Retrieves data from the local HomeWizard P1 device
        """
        headers = {"Accept": "application/json"}

        async with httpx.AsyncClient(headers=headers) as client:
            try:
                response = await client.get(self.api_url)
                response.raise_for_status()
            except httpx.HTTPError:
                content = response.content
                try:
                    error = HomeWizardErrorResponse.model_validate_json(content)
                    logger.error(str(error))
                except ValidationError:
                    logger.error("Unknown error occurred")

                return None

        try:
            data = HomeWizardP1Response.model_validate_json(response.content).to_p1data()
            logger.debug(data)
            return data
        except ValidationError:
            logger.error("Received unexpected content")
            return None
