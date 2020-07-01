#!/usr/bin/env python3
from multiprocessing import get_context
import sys
import time
from unittest import main, mock, TestCase

from tracerface.trace_process import TraceProcess, WritableQueue


class TestWritableQueue(TestCase):
    def test_written_value_gets_put_in_writable_queue(self):
        queue = WritableQueue(ctx=get_context())
        queue.write('val')
        self.assertEqual(queue.get(), 'val')


class TesTraceProcess(TestCase):
    def test_get_value_returns_none_for_empty_trace_process(self):
        process = TraceProcess('dummy_args')
        self.assertEqual(process.get_output(), None)

    @mock.patch('tracerface.trace_process.Tool')
    def test_get_value_returns_value_from_tool(self, tool):
        def dummy_print():
            print('dummy_val')

        tool.return_value.run = dummy_print
        process = TraceProcess('dummy_args')
        process.start()
        process.join()
        self.assertEqual(process.get_output(), 'dummy_val')

    @mock.patch('tracerface.trace_process.Tool')
    def test_get_value_strips_spaces(self, tool):
        def dummy_print():
            print('         dummy_val         ')

        tool.return_value.run = dummy_print
        process = TraceProcess('dummy_args')
        process.start()
        process.join()
        self.assertEqual(process.get_output(), 'dummy_val')

    @mock.patch('tracerface.trace_process.Tool')
    def test_get_value_keeps_empty_line(self, tool):
        def dummy_print():
            print('\n')

        tool.return_value.run = dummy_print
        process = TraceProcess('dummy_args')
        process.start()
        process.join()
        self.assertEqual(process.get_output(), '\n')


if __name__ == '__main__':
    main()
