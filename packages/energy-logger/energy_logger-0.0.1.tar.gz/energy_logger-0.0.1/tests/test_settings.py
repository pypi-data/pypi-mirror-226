from ipaddress import IPv4Address

from energy_logger.settings import get_settings


def test_get_settings_with_file(tmp_path):
    file = tmp_path / 'config.toml'
    file.write_text('[inputs.homewizard_p1]\nipaddress = "127.0.0.1"')

    settings = get_settings(file)
    assert settings.inputs.homewizard_p1.ipaddress == IPv4Address('127.0.0.1')


def test_get_settings_with_dict():
    settings = get_settings(data={
        'inputs': {
            'homewizard_p1': {
                'ipaddress': '127.0.0.1',
            }
        }
    })
    assert settings.inputs.homewizard_p1.ipaddress == IPv4Address('127.0.0.1')


def test_get_settings_with_str():
    settings = get_settings(data='[inputs.homewizard_p1]\nipaddress = "127.0.0.1"')
    assert settings.inputs.homewizard_p1.ipaddress == IPv4Address('127.0.0.1')
