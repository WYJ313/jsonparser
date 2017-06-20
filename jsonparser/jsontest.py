#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from jsonparser import JsonParser
from jsonexcept import JsonFormatException

class TestJsonParser(unittest.TestCase):

    """
    teststring是Json测试字符串
    testdict是teststring手工构造的对应字典
    """
    def setUp(self):
        self.teststring = '''
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
        self.testdict = {'name': 'wangyijun', 'true': True, 'false': False, 'none': None,\
                             'int': 56, 'float': 12.3, 'list': [1, 2, 3, 4, 5],\
                             'dict': {'dict1': 'hello', 'dict2': 'world'}}

    def test_load(self):
        js = JsonParser()
        js.load(self.teststring)
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_double_load(self):     # 证明两次load的有效性
        js = JsonParser()
        js.load(self.teststring)
        js.load(self.teststring)
        self.assertDictEqual(js._data, self.testdict)

    def test_dump(self):
        js = JsonParser()
        js.load(self.teststring)
        js.load(js.dump())
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_load_file(self):
        js = JsonParser()
        input = 'D:\\testin'
        js.load_file(input)
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_double_load_file(self):        # 证明两次load_file的有效性
        js = JsonParser()
        input = 'D:\\testin'
        js.load_file(input)
        js.load_file(input)
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_dump_file(self):
        js = JsonParser()
        input = 'D:\\testin'
        output = 'D:\\testout'
        js.load_file(input)
        js.dump_file(output)
        js.load_file(output)
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_load_dict(self):
        js = JsonParser()
        js.load_dict(self.testdict)
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_double_load_dict(self):        # 证明两次load_dict的有效性
        js = JsonParser()
        js.load_dict(self.testdict)
        js.load_dict(self.testdict)
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_dump_dict(self):
        js = JsonParser()
        js.load(self.teststring)
        print(js.dump_dict())
        tmp = self.teststring.replace('\n', '').replace('\r', '').replace('\t', '').replace('\b', '').replace('\f', '')
        print(tmp)
        self.assertEqual(js.dump(), tmp)

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
        js.update(self.testdict)
        print(js._data)
        print(self.testdict)
        self.assertDictEqual(js._data, self.testdict)


