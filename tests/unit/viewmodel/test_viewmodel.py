import unittest.mock as mock

from viewmodel.viewmodel import ViewModel


@mock.patch('viewmodel.viewmodel.BaseModel')
def test_viewmodel_initialization(basemodel):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel._configuration == configuration
    assert viewmodel._model == basemodel.return_value


@mock.patch('viewmodel.viewmodel.BaseModel.get_nodes', return_value={
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}})
def test_get_nodes_returns_nodes_from_model(get_nodes):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_nodes() == [
             {'data': {'count': 0,
                       'id': 'dummy_hash1',
                       'name': 'dummy_name1',
                       'source': 'dummy_source1'}},
             {'data': {'count': 1,
                       'id': 'dummy_hash2',
                       'name': 'dummy_name2',
                       'source': 'dummy_source2'}}]


@mock.patch('viewmodel.viewmodel.BaseModel.get_nodes', return_value={
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1},
        'dummy_hash3': {'name': 'dummy_name3', 'source': 'dummy_source1', 'call_count': 2}})
@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash1', 'dummy_hash2'): {'params': [], 'call_count': 0},
        ('dummy_hash1', 'dummy_hash3'): {'params': [['dummy_param']], 'call_count': 3},
        ('dummy_hash2', 'dummy_hash3'): {'params': [['dummy_param1'], ['dummy_param2'], ['dummy_param3']], 'call_count': 4}})
def test_get_edges_returns_nodes_from_model(get_edges, get_nodes):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_edges() == [
             {'data': {'call_count': 0,
                       'called_name': 'dummy_name2',
                       'caller_name': 'dummy_name1',
                       'params': '',
                       'source': 'dummy_hash1',
                       'target': 'dummy_hash2'}},
             {'data': {'call_count': 3,
                       'called_name': 'dummy_name3',
                       'caller_name': 'dummy_name1',
                       'params': 'dummy_param',
                       'source': 'dummy_hash1',
                       'target': 'dummy_hash3'}},
             {'data': {'call_count': 4,
                       'called_name': 'dummy_name3',
                       'caller_name': 'dummy_name2',
                       'params': '...',
                       'source': 'dummy_hash2',
                       'target': 'dummy_hash3'}}]


@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash1', 'dummy_hash2'): {'params': [], 'call_count': 0}})
def test_get_param_visuals_for_edge_returns_empty_string_with_no_params(get_edges):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_param_visuals_for_edge(('dummy_hash1', 'dummy_hash2')) == ''


@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash1', 'dummy_hash3'): {'params': [['dummy_param']], 'call_count': 3}})
def test_get_param_visuals_for_edge_returns_param_with_single_param(get_edges):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_param_visuals_for_edge(('dummy_hash1', 'dummy_hash3')) == 'dummy_param'


@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash2', 'dummy_hash3'): {'params': [['dummy_param1'], ['dummy_param2'], ['dummy_param3']], 'call_count': 4}})
def test_get_param_visuals_for_edge_returns_dots_with_multiple_params(get_edges):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_param_visuals_for_edge(('dummy_hash2', 'dummy_hash3')) == '...'


@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash2', 'dummy_hash3'): {'params': [], 'call_count': 4}})
def test_get_params_of_edge_returns_no_params(get_edges):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_params_of_edge('dummy_hash2', 'dummy_hash3') == []


@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash2', 'dummy_hash3'): {'params': [['dummy_param']], 'call_count': 4}})
def test_get_params_of_edge_returns_single_params(get_edges):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_params_of_edge('dummy_hash2', 'dummy_hash3') == [['dummy_param']]


@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash2', 'dummy_hash3'): {'params': [['dummy_param1'], ['dummy_param2'], ['dummy_param3']], 'call_count': 4}})
def test_get_params_of_edge_returns_multiple_params(get_edges):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_params_of_edge('dummy_hash2', 'dummy_hash3') == [['dummy_param1'], ['dummy_param2'], ['dummy_param3']]


@mock.patch('viewmodel.viewmodel.BaseModel.get_nodes', return_value={
        'dummy_hash3': {'name': 'dummy_name3', 'source': 'dummy_source1', 'call_count': 2}})
@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash1', 'dummy_hash3'): {'params': [['dummy_param']], 'call_count': 3}})
def test_get_params_of_node_returns_params_from_single_source(get_edges, get_nodes):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_params_of_node('dummy_hash3') == [['dummy_param']]


@mock.patch('viewmodel.viewmodel.BaseModel.get_nodes', return_value={
        'dummy_hash3': {'name': 'dummy_name3', 'source': 'dummy_source1', 'call_count': 2}})
@mock.patch('viewmodel.viewmodel.BaseModel.get_edges', return_value={
        ('dummy_hash1', 'dummy_hash3'): {'params': [['dummy_param']], 'call_count': 3},
        ('dummy_hash2', 'dummy_hash3'): {'params': [['dummy_param1'], ['dummy_param2'], ['dummy_param3']], 'call_count': 4}})
def test_get_params_of_node_returns_params_from_multiple_sources(get_edges, get_nodes):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.get_params_of_node('dummy_hash3') == [['dummy_param'], ['dummy_param1'], ['dummy_param2'], ['dummy_param3']]


@mock.patch('viewmodel.viewmodel.BaseModel.yellow_count', return_value=4)
def test_yellow_count_returns_count_from_model(yellow_count):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.yellow_count() == 4


@mock.patch('viewmodel.viewmodel.BaseModel.red_count', return_value=4)
def test_red_count_returns_count_from_model(red_count):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.red_count() == 4


@mock.patch('viewmodel.viewmodel.BaseModel.max_count', return_value=4)
def test_max_count_returns_count_from_model(max_count):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    assert viewmodel.max_count() == 4


@mock.patch('viewmodel.viewmodel.StaticModel')
def test_output_submit_btn_clicked_uses_static_model(static):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    viewmodel.output_submit_btn_clicked('dummy text')

    assert viewmodel._model == static.return_value
    static.return_value.load_text.assert_called_once()
    static.return_value.load_text.assert_called_with('dummy text')


@mock.patch('viewmodel.viewmodel.DynamicModel')
def test_trace_with_ui_elements_uses_dynamic_model(dynamic):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    viewmodel.trace_with_ui_elements('dummy dict')

    assert viewmodel._model == dynamic.return_value
    dynamic.return_value.trace_dict.assert_called_once()
    dynamic.return_value.trace_dict.assert_called_with('dummy dict')


@mock.patch('viewmodel.viewmodel.DynamicModel')
def test_trace_with_config_file_uses_dynamic_model(dynamic):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)

    viewmodel.trace_with_config_file('dummy path')

    assert viewmodel._model == dynamic.return_value
    dynamic.return_value.trace_yaml.assert_called_once()
    dynamic.return_value.trace_yaml.assert_called_with('dummy path')


@mock.patch('viewmodel.viewmodel.DynamicModel')
def test_trace_btn_turned_off_uses_dynamic_model(dynamic):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration)
    viewmodel._model = dynamic.return_value

    viewmodel.trace_btn_turned_off()

    dynamic.return_value.stop_trace.assert_called_once()


@mock.patch('viewmodel.viewmodel.BaseModel')
def test_set_range_uses_model(model):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)

    viewmodel.set_range('dummy', 'range')

    model.return_value.set_range.assert_called_once()
    model.return_value.set_range.assert_called_with('dummy', 'range')


@mock.patch('viewmodel.viewmodel.BaseModel')
def test_save_bcc_command_uses_model(model):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)

    viewmodel.save_bcc_command('dummy_command')

    model.return_value.save_bcc_command.assert_called_once()
    model.return_value.save_bcc_command.assert_called_with('dummy_command')


@mock.patch('viewmodel.viewmodel.BaseModel')
def test_save_layout_config_uses_model(model):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)

    viewmodel.save_layout_config('dummy_animate', 'dummy_layout')

    model.return_value.save_layout_config.assert_called_once()
    model.return_value.save_layout_config.assert_called_with('dummy_animate', 'dummy_layout')


@mock.patch('viewmodel.viewmodel.BaseModel.get_animate_config', return_value='dummy_animate')
def test_get_animate_config_uses_model(model):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)

    assert viewmodel.get_animate_config() == 'dummy_animate'


@mock.patch('viewmodel.viewmodel.BaseModel.get_spacing_config', return_value='dummy_spacing')
def test_get_spacing_config_uses_model(model):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)

    assert viewmodel.get_spacing_config() == 'dummy_spacing'


@mock.patch('viewmodel.viewmodel.DynamicModel.thread_error', return_value='dummy_error')
@mock.patch('viewmodel.viewmodel.DynamicModel')
def test_thread_error_uses_model(model, error):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)
    viewmodel._model = model

    assert viewmodel.thread_error() == 'dummy_error'


@mock.patch('viewmodel.viewmodel.DynamicModel.process_error', return_value='dummy_error')
@mock.patch('viewmodel.viewmodel.DynamicModel')
def test_process_error_uses_model(model, error):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)
    viewmodel._model = model

    assert viewmodel.process_error() == 'dummy_error'


@mock.patch('viewmodel.viewmodel.DynamicModel.trace_active', return_value='dummy_status')
@mock.patch('viewmodel.viewmodel.DynamicModel')
def test_trace_active_uses_model(model, error):
    configuration = mock.Mock()
    viewmodel = ViewModel(configuration.return_value)
    viewmodel._model = model

    assert viewmodel.trace_active() == 'dummy_status'
