# import threading
import trio

from energy_logger.inputs.homewizard.p1.input import HomeWizardP1Input
from energy_logger.inputs.util import get_active_inputs
#
#
# from energy_logger.homewizard.p1.client import get_data
#
#
# async def call():
#     await get_data()
#
#
# def loop() -> None:
#     timer = threading.Timer(5.0, call)
#     timer.daemon = True
#     timer.start()
# from energy_logger.homewizard.p1.data import get_data
from energy_logger.settings import get_settings


def main():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    settings = get_settings('energy-logger.toml.example')
    active_inputs = get_active_inputs(settings)

    for name, _input in active_inputs.items():
        trio.run(_input.read_data)


if __name__ == "__main__":
    main()
