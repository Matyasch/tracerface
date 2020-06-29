from pytest import fixture, raises
import unittest.mock as mock

from viewmodel.trace_setup import Setup
from viewmodel.viewmodel import ViewModel


@fixture
def nodes():
    return {
        'dummy_hash1': {
            'name': 'dummy_name1',
            'source': 'dummy_source1',
            'call_count': 0
        },
        'dummy_hash2': {
            'name': 'dummy_name2',
            'source': 'dummy_source2',
            'call_count': 1
        },
        'dummy_hash3': {
            'name': 'dummy_name3',
            'source': 'dummy_source1',
            'call_count': 2
        }
    }


@fixture
def edges():
    return {
        ('dummy_hash1', 'dummy_hash2'): {
            'params': [],
            'call_count': 0
        },
        ('dummy_hash1', 'dummy_hash3'): {
            'params': [['dummy_param']],
            'call_count': 3
        },
        ('dummy_hash2', 'dummy_hash3'): {
            'params': [['dummy_param1'], ['dummy_param2'], ['dummy_param3']],
            'call_count': 4
        }
    }


@mock.patch('viewmodel.viewmodel.Model')
def test_viewmodel_initialization(model):
    setup = Setup()
    viewmodel = ViewModel(setup)

    assert viewmodel._model == model.return_value
    assert viewmodel._setup == setup


@mock.patch('viewmodel.viewmodel.Model')
def test_get_nodes(model, nodes, edges):
    model.return_value.get_nodes.return_value = nodes
    setup = Setup()
    viewmodel = ViewModel(setup)

    assert viewmodel.get_nodes() == [
        {'data': {
            'count': 0,
            'id': 'dummy_hash1',
            'info': 'dummy_name1\nSource: dummy_source1\nCalled 0 times',
            'name': 'dummy_name1',
            'source': 'dummy_source1'
        }},
        {'data': {'count': 1,
            'id': 'dummy_hash2',
            'info': 'dummy_name2\nSource: dummy_source2\nCalled 1 times',
            'name': 'dummy_name2',
            'source': 'dummy_source2'
        }},
        {'data': {
            'count': 2,
            'id': 'dummy_hash3',
            'info': 'dummy_name3\nSource: dummy_source1\nCalled 2 times',
            'name': 'dummy_name3',
            'source': 'dummy_source1'
        }}
    ]


@mock.patch('viewmodel.viewmodel.Model')
def test_get_edges(model, nodes, edges):
    model.return_value.get_nodes.return_value = nodes
    model.return_value.get_edges.return_value = edges
    setup = Setup()
    viewmodel = ViewModel(setup)

    assert viewmodel.get_edges() == [
        {'data': {
            'call_count': 0,
            'called_name': 'dummy_name2',
            'caller_name': 'dummy_name1',
            'params': '',
            'source': 'dummy_hash1',
            'target': 'dummy_hash2',
            'info': 'Call made 0 times',
        }},
        {'data': {
            'call_count': 3,
            'called_name': 'dummy_name3',
            'caller_name': 'dummy_name1',
            'params': 'dummy_param',
            'source': 'dummy_hash1',
            'target': 'dummy_hash3',
            'info': 'Call made 3 times\nWith parameters:\ndummy_param'
        }},
        {'data': {
            'call_count': 4,
            'called_name': 'dummy_name3',
            'caller_name': 'dummy_name2',
            'params': '...',
            'source': 'dummy_hash2',
            'target': 'dummy_hash3',
            'info': 'Call made 4 times\nWith parameters:\ndummy_param1\ndummy_param2\ndummy_param3'
        }}
    ]


@mock.patch('viewmodel.viewmodel.Model')
def test_get_param_visuals(model, edges):
    model.return_value.get_edges.return_value = edges
    setup = Setup()
    viewmodel = ViewModel(setup)

    assert viewmodel.get_param_visuals_for_edge(('dummy_hash1', 'dummy_hash2')) == ''
    assert viewmodel.get_param_visuals_for_edge(('dummy_hash1', 'dummy_hash3')) == 'dummy_param'
    assert viewmodel.get_param_visuals_for_edge(('dummy_hash2', 'dummy_hash3')) == '...'


@mock.patch('viewmodel.viewmodel.Model')
def test_get_params_of_edge(model, edges):
    model.return_value.get_edges.return_value = edges
    setup = Setup()
    viewmodel = ViewModel(setup)

    assert viewmodel.get_params_of_edge('dummy_hash1', 'dummy_hash2') == []
    assert viewmodel.get_params_of_edge('dummy_hash1', 'dummy_hash3') == [['dummy_param']]
    assert viewmodel.get_params_of_edge('dummy_hash2', 'dummy_hash3') == [
        ['dummy_param1'], ['dummy_param2'], ['dummy_param3']
    ]


@mock.patch('viewmodel.viewmodel.Model')
def test_get_params_of_node(model, edges, nodes):
    model.return_value.get_nodes.return_value = nodes
    model.return_value.get_edges.return_value = edges
    setup = Setup()
    viewmodel = ViewModel(setup)

    assert viewmodel.get_params_of_node('dummy_hash2') == []
    assert viewmodel.get_params_of_node('dummy_hash3') == [
        ['dummy_param'], ['dummy_param1'], ['dummy_param2'], ['dummy_param3']
    ]


@mock.patch('viewmodel.viewmodel.Model')
def test_color_counts_return_value_from_model(model):
    model.return_value.yellow_count.return_value = 4
    model.return_value.red_count.return_value = 4
    model.return_value.max_count.return_value = 4

    setup = Setup()
    viewmodel = ViewModel(setup)

    assert viewmodel.yellow_count() == 4
    assert viewmodel.red_count() == 4
    assert viewmodel.max_count() == 4


@mock.patch('viewmodel.viewmodel.Path.read_text')
def test_load_output_from_directory(read):
    def side_effect():
        raise IsADirectoryError

    read.side_effect = side_effect
    setup = Setup()
    viewmodel = ViewModel(setup)

    with raises(ValueError):
        viewmodel.load_output('/direcory/path')


@mock.patch('viewmodel.viewmodel.Path.read_text')
def test_load_output_from_directory(read):
    def side_effect():
        raise FileNotFoundError

    read.side_effect = side_effect
    setup = Setup()
    viewmodel = ViewModel(setup)

    with raises(ValueError):
        viewmodel.load_output('.non/existent/path')


@mock.patch('viewmodel.viewmodel.Path.read_text', return_value='dummy text')
@mock.patch('viewmodel.viewmodel.Model')
def test_load_output_uses_model(model, read):
    setup = Setup()
    viewmodel = ViewModel(setup)

    viewmodel.load_output('dummy path')

    assert viewmodel._model == model.return_value
    model.return_value.load_output.assert_called_once()
    model.return_value.load_output.assert_called_with('dummy text')


@mock.patch('viewmodel.viewmodel.Model')
def test_start_trace_uses_model(model):
    setup = mock.Mock()
    setup.generate_bcc_args.return_value = 'dummy args'
    viewmodel = ViewModel(setup)

    viewmodel.start_trace()

    assert viewmodel._model == model.return_value
    model.return_value.start_trace.assert_called_once()
    model.return_value.start_trace.assert_called_with('dummy args')


@mock.patch('viewmodel.viewmodel.Model')
def test_stop_trace_uses_model(model):
    setup = Setup()
    viewmodel = ViewModel(setup)
    viewmodel._model = model.return_value

    viewmodel.stop_trace()

    model.return_value.stop_trace.assert_called_once()


@mock.patch('viewmodel.viewmodel.Model')
def test_set_range_uses_model(model):
    setup = Setup()
    viewmodel = ViewModel(setup)

    viewmodel.set_range('dummy', 'range')

    model.return_value.set_range.assert_called_once()
    model.return_value.set_range.assert_called_with('dummy', 'range')


@mock.patch('viewmodel.viewmodel.Model.thread_error', return_value='dummy_error')
@mock.patch('viewmodel.viewmodel.Model')
def test_thread_error_uses_model(model, error):
    setup = Setup()
    viewmodel = ViewModel(setup)
    viewmodel._model = model

    assert viewmodel.thread_error() == 'dummy_error'


@mock.patch('viewmodel.viewmodel.Model.process_error', return_value='dummy_error')
@mock.patch('viewmodel.viewmodel.Model')
def test_process_error_uses_model(model, error):
    setup = Setup()
    viewmodel = ViewModel(setup)
    viewmodel._model = model

    assert viewmodel.process_error() == 'dummy_error'


@mock.patch('viewmodel.viewmodel.Model.trace_active', return_value='dummy_status')
@mock.patch('viewmodel.viewmodel.Model')
def test_trace_active_uses_model(model, error):
    setup = Setup()
    viewmodel = ViewModel(setup)
    viewmodel._model = model

    assert viewmodel.trace_active() == 'dummy_status'


def test_add_app_leaves_setup_untouched_with_invalid_arguments():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.add_app(None)
    assert not setup.initialize_app.called


def test_add_app_adds_app_as_binary_to_setup_if_no_exception_happens():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)
    viewmodel.add_app('app')
    setup.initialize_binary.assert_called_with('app')


def test_add_app_adds_app_as_built_in_to_setup_exception_happens():
    setup = mock.Mock()
    setup.initialize_binary.side_effect = ValueError()
    viewmodel = ViewModel(setup)
    viewmodel.add_app('app')
    setup.initialize_binary.assert_called_with('app')
    setup.initialize_built_in.assert_called_with('app')


def test_remove_app():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.remove_app(None)
    assert not setup.remove_app.called

    viewmodel.remove_app('app')
    setup.remove_app.assert_called_with('app')


def test_get_apps():
    setup = mock.Mock()
    setup.get_apps.return_value = 'dummy apps'
    viewmodel = ViewModel(setup)

    assert viewmodel.get_apps() == 'dummy apps'


def test_get_traced_functions_for_app():
    setup = mock.Mock()
    setup.get_setup_of_app.return_value = {
        'func1': {'traced': True},
        'func2': {'traced': False}
    }
    viewmodel = ViewModel(setup)

    assert viewmodel.get_traced_functions_for_app(None) == []
    assert viewmodel.get_traced_functions_for_app('dummy') == ['func1']


def test_get_not_traced_functions_for_app():
    setup = mock.Mock()
    setup.get_setup_of_app.return_value = {
        'func1': {'traced': True},
        'func2': {'traced': False}
    }
    viewmodel = ViewModel(setup)

    assert viewmodel.get_not_traced_functions_for_app(None) == []
    assert viewmodel.get_not_traced_functions_for_app('dummy') == ['func2']


def test_add_function_leaves_setup_untouched_with_invalid_arguments():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.add_function(None, None)
    viewmodel.add_function('app', None)
    viewmodel.add_function(None, 'func')
    assert not setup.add_function.called


def test_add_function_adds_function_to_setup():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.add_function('app', 'func')
    setup.setup_function_to_trace.assert_called_with('app', 'func')


def test_remove_function_leaves_setup_untouched_with_invalid_arguments():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.remove_function(None, None)
    viewmodel.remove_function('app', None)
    viewmodel.remove_function(None, 'func')
    assert not setup.remove_function_from_trace.called


def test_remove_function_removes_function_from_setup():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.remove_function('app', 'func')
    setup.remove_function_from_trace.assert_called_with('app', 'func')


def test_get_parameters():
    setup = mock.Mock()
    setup.get_parameters.return_value = 'dummy params'
    viewmodel = ViewModel(setup)

    assert viewmodel.get_parameters(None, None) == {}
    assert viewmodel.get_parameters('app', 'func') == 'dummy params'


def test_add_parameter():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.add_parameter(None, None, None, None)
    assert not setup.add_parameter.called

    viewmodel.add_parameter('app', 'func', '0', 'format')
    setup.add_parameter.assert_called_with('app', 'func', '0', 'format')


def test_remove_parameter():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.remove_parameter(None, None, None)
    assert not setup.remove_parameter.called

    viewmodel.remove_parameter('app', 'func', '0')
    setup.remove_parameter.assert_called_with('app', 'func', 0)


def test_expanded_elements():
    setup = mock.Mock()
    viewmodel = ViewModel(setup)

    viewmodel.element_clicked('dummy_id1')
    assert 'dummy_id1' in viewmodel._expanded_elements

    viewmodel.element_clicked('dummy_id2')
    assert 'dummy_id1' in viewmodel._expanded_elements
    assert 'dummy_id2' in viewmodel._expanded_elements

    viewmodel.element_clicked('dummy_id1')
    assert 'dummy_id1' not in viewmodel._expanded_elements
