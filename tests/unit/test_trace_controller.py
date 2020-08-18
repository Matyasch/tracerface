#!/usr/bin/env python3
from unittest import main, mock, TestCase

from tracerface.trace_controller import TraceController


class TestTraceController(TestCase):
    @mock.patch('tracerface.trace_controller.Thread')
    @mock.patch('tracerface.trace_controller.TraceProcess')
    def test_start_trace_happy_case(self, process, thread):
        trace_controller = TraceController()

        trace_controller.start_trace(['dummy', 'functions'], mock.Mock())

        self.assertIsNone(trace_controller.thread_error())
        self.assertTrue(trace_controller._thread_enabled)
        process.assert_called_once_with(args=['', '-UK', 'dummy', 'functions'])


    def test_start_trace_without_functions(self):
        trace_controller = TraceController()
        trace_controller.start_trace([], mock.Mock())

        self.assertEqual(trace_controller.thread_error(), 'No functions to trace')


    def test_stop_trace_disables_thread(self):
        trace_controller = TraceController()
        trace_controller._thread_enabled = True
        trace_controller.stop_trace()
        self.assertFalse(trace_controller._thread_enabled)


    def test_thread_error_returns_error(self):
        trace_controller = TraceController()
        trace_controller._thread_error = 'Dummy Error'

        self.assertEqual(trace_controller.thread_error(), 'Dummy Error')


if __name__ == '__main__':
    main()
