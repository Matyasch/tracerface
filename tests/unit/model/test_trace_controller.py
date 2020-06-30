from unittest import main, mock, TestCase

from model.trace_controller import TraceController


class TestTraceController(TestCase):
    @mock.patch('model.trace_controller.Thread')
    @mock.patch('model.trace_controller.TraceProcess')
    def test_start_trace_happy_case(self, process, thread):
        trace_controller = TraceController(mock.Mock())

        trace_controller.start_trace(['dummy', 'functions'])

        self.assertIsNone(trace_controller.thread_error())
        self.assertTrue(trace_controller.trace_active())
        process.assert_called_once_with(args=['', '-UK', 'dummy', 'functions'])


    def test_start_trace_without_functions(self):
        trace_controller = TraceController(mock.Mock())
        trace_controller.start_trace([])

        self.assertEqual(trace_controller.thread_error(), 'No functions to trace')


    def test_stop_trace_disables_thread(self):
        trace_controller = TraceController(mock.Mock())
        trace_controller._thread_enabled = True
        trace_controller.stop_trace()
        self.assertFalse(trace_controller.trace_active())


    def test_thread_error_returns_error(self):
        trace_controller = TraceController(mock.Mock())
        trace_controller._thread_error = 'Dummy Error'

        self.assertEqual(trace_controller.thread_error(), 'Dummy Error')


    def test_trace_active_returns_thread_enabled(self):
        trace_controller = TraceController(mock.Mock())
        trace_controller._thread_enabled = True

        self.assertTrue(trace_controller.trace_active())


if __name__ == '__main__':
    main()
