from typing import Protocol

from pydantic_settings import BaseSettings

from energy_logger.models import BaseData


class InputProtocol(Protocol):
    """This Protocol defines what an input source should look like"""
    settings: BaseSettings

    async def read_data(self) -> BaseData:
        """Reads data from the input"""
        ...
