from unittest.mock import Mock, patch

from model.base import BaseModel


@patch("model.base.Persistence")
def test_initialization(persistence):
    config = Mock()
    model = BaseModel(config)

    assert model._persistence is persistence.return_value
    assert model._configuration is config


@patch("model.base.Persistence")
def test_get_nodes_gets_nodes_from_persistence(persistence):
    model = BaseModel(None)

    model.get_nodes()

    persistence.return_value.get_nodes.assert_called_once()


@patch("model.base.Persistence")
def test_get_edges_gets_edges_from_persistence(persistence):
    model = BaseModel(None)

    model.get_edges()

    persistence.return_value.get_edges.assert_called_once()


@patch("model.base.Persistence")
def test_yellow_count_gets_range_from_persistence(persistence):
    model = BaseModel(None)

    model.yellow_count()

    persistence.return_value.get_yellow.assert_called_once()


@patch("model.base.Persistence")
def test_red_count_gets_range_from_persistence(persistence):
    model = BaseModel(None)

    model.red_count()

    persistence.return_value.get_red.assert_called_once()


@patch("model.base.Persistence")
def test_max_count_gets_range_from_persistence(persistence):
    model = BaseModel(None)

    model.max_count()

    persistence.return_value.get_top.assert_called_once()


@patch("model.base.Persistence")
def test_set_range_calls_persistence_with_right_params(persistence):
    model = BaseModel(None)

    model.set_range('dummy_yellow', 'dummy_red')

    persistence.return_value.update_color_range.assert_called_once()
    persistence.return_value.update_color_range.assert_called_with('dummy_yellow', 'dummy_red')


def test_save_app_config_calls_configuration_with_right_params():
    config = Mock()
    model = BaseModel(config)

    model.save_app_config('dummy_command')

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

    model.get_spacing_config()

    config.get_spacing.assert_called_once()


def test_get_animate_config_calls_configuration():
    config = Mock()
    model = BaseModel(config)

    model.get_animate_config()

    config.get_animate.assert_called_once()