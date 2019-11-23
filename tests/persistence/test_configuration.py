from pytest import raises

from persistence.configuration import Configuration


def test_initial_config():
    config = Configuration()

    assert config._bcc_command == 'trace-bpfcc'
    assert config._animate
    assert config._spacing == 2


def test_update_command():
    config = Configuration()

    config.update_command('dummy_command')

    assert config._bcc_command == 'dummy_command'
    assert config._animate
    assert config._spacing == 2


def test_update_layout_by_valid_values():
    config = Configuration()

    config.update_layout(False, 3)

    assert config._bcc_command == 'trace-bpfcc'
    assert not config._animate
    assert config._spacing == 3


def test_update_layout_by_invalid_values():
    config = Configuration()

    with raises(ValueError) as excinfo:
        config.update_layout(False, 0)

    assert str(excinfo.value) == 'Spacing can not be less than 1'


def test_get_spacing_returns_spacing():
    config = Configuration()
    config._spacing = 10

    assert config.get_spacing() == 10


def test_get_animate_returns_animate():
    config = Configuration()
    config._animate = False

    assert not config.get_animate()


def test_get_command_returns_command():
    config = Configuration()
    config._bcc_command = 'dummy command'

    assert config.get_command() == 'dummy command'