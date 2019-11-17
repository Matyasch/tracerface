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


def test_update_layout():
    config = Configuration()
    config.update_layout(False, 3)
    assert config.bcc_command == 'trace-bpfcc'
    assert not config.animate
    assert config.spacing == 3