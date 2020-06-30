from pathlib import Path
from pytest import raises
from queue import Empty
from unittest import main, mock, TestCase

from model.model import Model
from model.parse_stack import Stack


class TestModel(TestCase):
    @mock.patch('model.model.Thread')
    @mock.patch('model.model.TraceProcess')
    def test_start_trace_happy_case(self, process, thread):
        model = Model(mock.Mock())

        model.start_trace(['dummy', 'functions'])

        self.assertIsNone(model.thread_error())
        self.assertTrue(model.trace_active())
        process.assert_called_once_with(args=['', '-UK', 'dummy', 'functions'])


    def test_start_trace_without_functions(self):
        model = Model(mock.Mock())
        model.start_trace([])

        self.assertEqual(model.thread_error(), 'No functions to trace')


    def test_stop_trace_disables_thread(self):
        model = Model(mock.Mock())
        model._thread_enabled = True
        model.stop_trace()
        self.assertFalse(model.trace_active())


    def test_thread_error_returns_error(self):
        model = Model(mock.Mock())
        model._thread_error = 'Dummy Error'

        self.assertEqual(model.thread_error(), 'Dummy Error')


    def test_trace_active_returns_thread_enabled(self):
        model = Model(mock.Mock())
        model._thread_enabled = True

        self.assertTrue(model.trace_active())


    def test_load_output(self):
        test_file_path = Path(__file__).absolute().parent.parent.parent.joinpath(
            'integration', 'resources', 'test_static_output'
        )
        text = test_file_path.read_text()
        call_graph = mock.Mock()
        call_graph.get_nodes.return_value = {}
        model = Model(call_graph)

        model.load_output(text)

        self.assertEqual(call_graph.load_nodes.call_count, 8)
        self.assertEqual(call_graph.load_edges.call_count, 8)


if __name__ == '__main__':
    main()
