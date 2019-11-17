import pytest

from persistence.configuration import Configuration


def test_initial_config():
    config = Configuration()
    assert config.bcc_command == 'trace-bpfcc'
    assert config.animate
    assert config.spacing == 2


def test_update_command():
    config = Configuration()
    config.update_command('dummy_command')
    assert config.bcc_command == 'dummy_command'
    assert config.animate
    assert config.spacing == 2


def test_update_layout_by_valid_values():
    config = Configuration()
    config.update_layout(False, 3)
    assert config.bcc_command == 'trace-bpfcc'
    assert not config.animate
    assert config.spacing == 3


def test_update_layout_by_invalid_values():
    config = Configuration()
    with pytest.raises(ValueError) as excinfo:   
        config.update_layout(False, 0)
    assert str(excinfo.value) == 'Spacing can not be less than 1'