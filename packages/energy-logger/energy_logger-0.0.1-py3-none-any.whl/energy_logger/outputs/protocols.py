from typing import Any, Protocol


class OutputProtocol(Protocol):
    """This Protocol defines what an output source should look like"""

    def write_data(self, data: Any) -> None:
        """Writes data to the output"""
        ...
