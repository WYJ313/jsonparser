#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from jsonparser import JsonParser

class TestJsonParser(unittest.TestCase):
    def setUp(self):
        self.testloadstring = '''
        {
"name":"wangyijun",
"true":true,
"false":false,
"none":none,
"int":56,
"float":12.3,
"list": [1, 2, 3, 4, 5],
"dict": {"dict1": "hello", "dict2": "world"}}
        '''
        self.testloaddict = {'name': 'wangyijun', 'true': True, 'false': False, 'none': None,\
                             'int': 56, 'float':12.3, 'list': [1, 2, 3, 4, 5],\
                             'dict': {'dict1': 'hello', 'dict2': 'world'}}


    def test_load(self):
        js = JsonParser()
        js.load(self.testloadstring)
        print(js._data)
        print(self.testloaddict)
        #self.assertDictEqual(js._data, self.testloaddict)

    def test_dump(self):
        js = JsonParser()
        js.load(self.testloadstring)
        js.load(js.dump())
        print(js._data)
        print(self.testloaddict)
        self.assertDictEqual(js._data, self.testloaddict)

    def test_load_file(self):
        js = JsonParser()
        path = 'D:\\testin'
        js.load_file(path)
        print(js._data)
        print(self.testloaddict)
        self.assertDictEqual(js._data, self.testloaddict)

    def test_dump_file(self):
        js = JsonParser()
        path = 'D:\\testout'
        js.load(self.testloadstring)
        js.dump_file(path)
        js.load_file(path)
        print(js._data)
        print(self.testloaddict)
        self.assertDictEqual(js._data, self.testloaddict)

    def test_load_dict(self):
        js = JsonParser()
        js.load_dict(self.testloaddict)
        print(js._data)
        print(self.testloaddict)
        self.assertDictEqual(js._data, self.testloaddict)

    def test_dump_dict(self):
        js = JsonParser()
        js.load(self.testloadstring)
        print(js.dump_dict())
        print(self.testloaddict)
        self.assertDictEqual(js.dump_dict(), self.testloaddict)

    def test_setitem(self):
        js = JsonParser()
        js['hello'] = 'world'
        print(js._data['hello'])
        print('world')
        self.assertEqual(js._data['hello'], 'world')

    def test_getitem(self):
        js = JsonParser()
        js['hello'] = 'world'
        print(js['hello'])
        print('world')
        self.assertEqual(js['hello'], 'world')

    def test_update(self):
        js = JsonParser()
        js.update(self.testloaddict)
        print(js._data)
        print(self.testloaddict)
        self.assertDictEqual(js._data, self.testloaddict)


