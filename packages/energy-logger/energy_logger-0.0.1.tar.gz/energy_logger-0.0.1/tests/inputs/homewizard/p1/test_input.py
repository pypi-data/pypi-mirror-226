from ipaddress import IPv4Address, IPv6Address
from pathlib import Path
from unittest.mock import patch

from pytest_httpx import HTTPXMock

from energy_logger.inputs.homewizard import HomeWizardP1Input
from energy_logger.inputs.homewizard.p1.settings import HomeWizardP1Settings
from energy_logger.models import P1Data

HOMEWIZARD_P1_SETTINGS = HomeWizardP1Settings(
    ipaddress='127.0.0.1'
)

DATA_DIR = Path(__file__).parent.joinpath('data/')


def test_homewizard_p1_input_ipaddress():
    # IPv4
    p1_input = HomeWizardP1Input(HOMEWIZARD_P1_SETTINGS)

    assert p1_input.ipaddress == IPv4Address('127.0.0.1')

    # IPv6
    p1_input = HomeWizardP1Input(
        settings=HomeWizardP1Settings(
            ipaddress='::1'
        )
    )

    assert p1_input.ipaddress == IPv6Address('::1')


def test_homewizard_p1_input_api_url():
    p1_input = HomeWizardP1Input(HOMEWIZARD_P1_SETTINGS)
    assert p1_input.api_url == 'http://127.0.0.1/api/v1/data/'


async def test_homewizard_p1_input_read_data(httpx_mock: HTTPXMock):
    p1_input = HomeWizardP1Input(HOMEWIZARD_P1_SETTINGS)

    with open(DATA_DIR / 'p1_200.json', 'rb') as f:
        httpx_mock.add_response(status_code=200, content=f.read())

    data = await p1_input.read_data()

    assert isinstance(data, P1Data)

async def test_homewizard_p1_input_read_data_invalid_data(httpx_mock):
    p1_input = HomeWizardP1Input(HOMEWIZARD_P1_SETTINGS)

    httpx_mock.add_response(status_code=200, content=b'{"foo": "bar"}')

    with patch('energy_logger.inputs.homewizard.p1.input.logger') as mock_logger:
        data = await p1_input.read_data()

    assert data is None
    mock_logger.error.assert_called_once_with(
        "Received unexpected content"
    )


async def test_homewizard_p1_input_read_data_http_error_unknown(httpx_mock):
    p1_input = HomeWizardP1Input(HOMEWIZARD_P1_SETTINGS)

    httpx_mock.add_response(status_code=400, content=b'{"error": "1"}')

    with patch('energy_logger.inputs.homewizard.p1.input.logger') as mock_logger:
        data = await p1_input.read_data()

    assert data is None
    mock_logger.error.assert_called_once_with(
        "Unknown error occurred"
    )


