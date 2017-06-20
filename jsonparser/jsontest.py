#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from jsonparser import JsonParser
from jsonexcept import JsonFormatException, JsonStringFormatException, JsonDictFormatException, \
    JsonNumberFormatException, JsonListFormatException, JsonConstantFormatException


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
            "dict": {"dict1": "hello", "dict2": "world"}
        }
        '''
        self.testdict = {'name': 'wangyijun', 'true': True, 'false': False, 'none': None,\
                             'int': 56, 'float': 12.3, 'list': [1, 2, 3, 4, 5],\
                             'dict': {'dict1': 'hello', 'dict2': 'world'}}

    def test_load(self):
        js = JsonParser()
        js.load(self.teststring)
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
        self.assertDictEqual(js._data, self.testdict)

    def test_load_file(self):
        js = JsonParser()
        input = './testin'
        js.load_file(input)
        self.assertDictEqual(js._data, self.testdict)

    def test_double_load_file(self):        # 证明两次load_file的有效性
        js = JsonParser()
        input = './testin'
        js.load_file(input)
        js.load_file(input)
        self.assertDictEqual(js._data, self.testdict)

    def test_dump_file(self):
        js = JsonParser()
        input = './testin'
        output = './testout'
        js.load_file(input)
        js.dump_file(output)
        js.load_file(output)
        self.assertDictEqual(js._data, self.testdict)

    def test_load_dict(self):
        js = JsonParser()
        js.load_dict(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_double_load_dict(self):        # 证明两次load_dict的有效性
        js = JsonParser()
        js.load_dict(self.testdict)
        js.load_dict(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_dump_dict(self):
        js = JsonParser()
        js.load(self.teststring)
        tmp = self.teststring.replace('\n', '').replace('\r', '').replace('\t', '').replace('\b', '').replace('\f', '')
        self.assertEqual(js.dump(), tmp)

    def test_setitem(self):
        js = JsonParser()
        js['hello'] = 'world'
        self.assertEqual(js._data['hello'], 'world')

    def test_getitem(self):
        js = JsonParser()
        js['hello'] = 'world'
        self.assertEqual(js['hello'], 'world')

    def test_update(self):
        js = JsonParser()
        js.update(self.testdict)
        self.assertDictEqual(js._data, self.testdict)

    def test_json_format_exception(self):
        test = '{"as": "hello", "bs": [problem, none, false], "cs": {"ds": true}}'
        js = JsonParser()
        try:
            js.load(test)
        except JsonFormatException as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_json_string_format_exception(self):
        test = '{"as": "hello" bs": ["problem", none, false], "cs": {"ds": true}}'
        js = JsonParser()
        try:
            js.load(test)
        except JsonStringFormatException:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_json_list_format_exception(self):
        test = '{"as": "hello", "bs":["problem", none, false, "cs": {"ds": true}}'
        js = JsonParser()
        try:
            js.load(test)
        except JsonListFormatException:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_json_dict_format_exception(self):
        test = '{"as": "hello", "bs": ["problem", none, false], "cs": {"ds": true}'
        js = JsonParser()
        try:
            js.load(test)
        except JsonDictFormatException:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_json_constant_exception(self):
        test = '{"as": "hello", "bs": ["problem", none, faLse], "cs": {"ds": true}}'
        js = JsonParser()
        try:
            js.load(test)
        except JsonConstantFormatException:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_json_number_format_exception(self):
        test = '{"as": "hello", "bs": [123.4.5, none, false], "cs": {"ds": true}}'
        js = JsonParser()
        try:
            js.load(test)
            print(js._data)
        except JsonNumberFormatException:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_IOError_load_file(self):
        try:
            js = JsonParser()
            input = './testint'
            js.load_file(input)
        except IOError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_IOError_dump_file(self):
        try:
            js = JsonParser()
            input = './testin'
            output = './tmp/testout'
            js.load_file(input)
            js.dump_file(output)
        except IOError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_parameter_type(self):
        try:
            js = JsonParser()
            s = '["as", "hello", "bs", [123.4.5, none, false], "cs", {"ds": true}]'
            js.load_dict(s)
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_key_type_setitem(self):
        try:
            js = JsonParser()
            js[123] = 'world'
        except KeyError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_key_type_setitem(self):
        try:
            js = JsonParser()
            js['hello'] = JsonParser()
        except ValueError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_key_invalid_getitem(self):
        try:
            js = JsonParser()
            print(js['hello'])
        except KeyError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)












