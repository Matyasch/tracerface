from multiprocessing import Queue
import time
import unittest.mock as mock

from model.trace_utils import AtomicStringIo, TraceProcess


def test_getvalue_removes_contents():
    string_io = AtomicStringIo()

    string_io.write('value 1')

    assert string_io.getvalue() == 'value 1'
    assert string_io.getvalue() == ''


def test_trace_process_initialization():
    queue = mock.Mock()
    args = mock.Mock()
    process = TraceProcess(queue, args)

    assert process._queue == queue
    assert process._args == args
    assert not process._alive


@mock.patch('model.trace_utils.Thread.start')
def test_trace_process_run(start):
    queue = mock.Mock()
    args = mock.Mock()
    process = TraceProcess(queue, args)
    process._run_bcc_trace = mock.Mock()

    process.run()

    start.assert_called()
    process._run_bcc_trace.assert_called()

def test_trace_process_put_middle_stack():
    def side_effect(*argv):
        process._alive = False
        return 'dummy value'

    string_io = mock.Mock()
    string_io.getvalue = mock.Mock(side_effect=side_effect)
    queue = mock.Mock()
    args = mock.Mock()
    process = TraceProcess(queue, args)
    process._alive = True

    process._put(string_io)

    assert not queue.put.called


def test_trace_process_put_end_of_stack():
    def side_effect(*argv):
        process._alive = False
        return 'dummy value\n\n'

    string_io = mock.Mock()
    string_io.getvalue = mock.Mock(side_effect=side_effect)
    queue = mock.Mock()
    args = mock.Mock()
    process = TraceProcess(queue, args)
    process._alive = True

    process._put(string_io)

    assert queue.put.called
