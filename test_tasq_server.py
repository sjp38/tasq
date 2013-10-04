#!/usr/bin/env python

import unittest
import tasq_server

task1 = {'cmd': 'enq', 'user': 'foo', 'path': '/home/cudat1/',
    'job': 'ls', 'output': 'out'}
task2 = {'cmd': 'enq', 'user': 'foo', 'path': '/home/cudat1/',
    'job': 'ls', 'output': 'out'}
task3 = {'cmd': 'enq', 'user': 'foo', 'path': '/home/cudat1/',
    'job': 'ls', 'output': 'out'}
task4 = {'cmd': 'enq', 'user': 'foo', 'path': '/home/cudat1/',
    'job': 'ls', 'output': 'out'}
task5 = {'cmd': 'enq', 'user': 'bar', 'path': '/home/cudat1/',
    'job': 'ls', 'output': 'out'}

class TestTasQServer(unittest.TestCase):
    def setUp(self):
        print "setup tasq_server test..."

    def tearDown(self):
        print "tear down..."

    def test_process_task(self):
        self.assertEqual(1, 1)
        pass

    def test_enq_task(self):
        tasq_server.tasks = []
        tasq_server.enq_task(task1)
        tasq_server.enq_task(task2)
        tasq_server.enq_task(task3)

        self.assertEqual(task1, tasq_server.tasks[0])
        self.assertEqual(task2, tasq_server.tasks[1])
        self.assertEqual(task3, tasq_server.tasks[2])

        self.assertFalse(tasq_server.enq_task(task4))

        self.assertTrue(tasq_server.enq_task(task5))


    def test_parse_msg(self):
        msg = ("enq_!@#_foouser_!@#_/home/foouser_!@#_" +
                "/usr/bin/gcc -o queued matmul.c" +
                "_!@#_out2")
        task = tasq_server.parse_msg(msg)
        self.assertEqual(task['cmd'], 'enq')
        self.assertEqual(task['user'], 'foouser')
        self.assertEqual(task['path'], '/home/foouser')
        self.assertEqual(task['job'], '/usr/bin/gcc -o queued matmul.c')
        self.assertEqual(task['out'], 'out2')

    def test_list_tasks(self):
        tasq_server.tasks = []
        tasq_server.enq_task(task1)
        tasq_server.enq_task(task2)
        tasq_server.enq_task(task5)
        tasq_server.enq_task(task3)
        listed = tasq_server.list_tasks('foo')
        self.assertEqual(listed,
                "Queue State: \n\tls\n\tls\n\tOthers Job\n\tls")
