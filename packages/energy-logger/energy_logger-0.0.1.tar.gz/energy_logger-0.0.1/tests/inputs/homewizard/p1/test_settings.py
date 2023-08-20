from ipaddress import IPv4Address

import pytest
from pydantic import ValidationError

from energy_logger.inputs.homewizard.p1.settings import HomeWizardP1Settings


def test_homewizard_p1_settings():
    settings = HomeWizardP1Settings(ipaddress='127.0.0.1')
    assert settings.ipaddress == IPv4Address('127.0.0.1')


def test_homewizard_p1_settings_invalid_ipaddress():
    with pytest.raises(ValidationError) as exc_info:
        HomeWizardP1Settings(ipaddress='wizard.local')

    assert "value is not a valid IPv4 or IPv6 address" in str(exc_info.value)
