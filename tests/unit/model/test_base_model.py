from unittest.mock import call, Mock, patch

from model.base import BaseModel


def test_empty_model():
    config = Mock()
    model = BaseModel(config)

    assert model._configuration is config
    assert model.get_edges() == {}
    assert model.get_nodes() == {}


@patch('model.base.Persistence')
def test_get_nodes_gets_nodes_from_persistence(persistence):
    model = BaseModel(None)

    model.get_nodes()

    persistence.return_value.get_nodes.assert_called_once()


@patch('model.base.Persistence')
def test_get_edges_gets_edges_from_persistence(persistence):
    model = BaseModel(None)

    model.get_edges()

    persistence.return_value.get_edges.assert_called_once()


@patch('model.base.Persistence')
def test_yellow_count_gets_range_from_persistence(persistence):
    model = BaseModel(None)

    model.yellow_count()

    persistence.return_value.get_yellow.assert_called_once()


@patch('model.base.Persistence')
def test_red_count_gets_range_from_persistence(persistence):
    model = BaseModel(None)

    model.red_count()

    persistence.return_value.get_red.assert_called_once()


@patch('model.base.Persistence.get_nodes')
def test_max_count_gets_with_no_nodes(get_nodes):
    model = BaseModel(None)

    assert model.max_count() == 0


@patch('model.base.Persistence.get_nodes', return_value={
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 2},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 5}
    })
def test_max_count_gets_with_nodes(get_nodes):
    model = BaseModel(None)

    assert model.max_count() == 5


@patch('model.base.Persistence')
def test_set_range_calls_persistence_with_right_params(persistence):
    model = BaseModel(None)

    model.set_range('dummy_yellow', 'dummy_red')

    persistence.return_value.update_colors.assert_called_once()
    persistence.return_value.update_colors.assert_called_with('dummy_yellow', 'dummy_red')


def test_save_bcc_command_calls_configuration_with_right_params():
    config = Mock()
    model = BaseModel(config)

    model.save_bcc_command('dummy_command')

    config.update_command.assert_called_once()
    config.update_command.assert_called_with('dummy_command')


def test_save_layout_config_calls_configuration_with_right_params():
    config = Mock()
    model = BaseModel(config)

    model.save_layout_config('dummy_animate', 'dummy_spacing')

    config.update_layout.assert_called_once()
    config.update_layout.assert_called_with('dummy_animate', 'dummy_spacing')


def test_get_spacing_config_calls_configuration():
    config = Mock()
    model = BaseModel(config)
    config.get_spacing.return_value = 'Dummy Value'

    assert model.get_spacing_config() == 'Dummy Value'


def test_get_animate_config_calls_configuration():
    config = Mock()
    config.get_animate.return_value = 'Dummy Value'
    model = BaseModel(config)

    assert model.get_animate_config() == 'Dummy Value'


@patch('model.base.Persistence')
def test_init_colors(persistence):
    model = BaseModel(None)
    model.max_count = Mock(return_value=8)

    model.init_colors()

    assert model.max_count.call_count == 2
    persistence.return_value.update_colors.assert_called_once()
    persistence.return_value.update_colors.assert_called_with(3, 5)
