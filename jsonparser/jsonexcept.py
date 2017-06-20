#!/usr/bin/env python
# -*- coding: utf-8 -*-


class JsonException(Exception):
    pass


class JsonFormatException(JsonException):
    def __init__(self, s):
        self.message = '未知格式错误，当前错误数据：' + s


class JsonStringFormatException(JsonFormatException):
    def __init__(self, s):
        self.message =  '字符串请用"xx"格式，当前错误数据：' + s


class JsonListFormatException(JsonFormatException):
    def __init__(self, s):
        self.message =  '列表请用[xx, ...]格式，当前错误数据：' + s


class JsonDictFormatException(JsonFormatException):
    def __init__(self, s):
        self.message = '字典请用{xx: xxx, ...}格式，当前错误数据：' + s


class JsonNumberFormatException(JsonFormatException):
    def __init__(self, s):
        self.message = '数字请用xx, -xx, xx.xx格式，当前错误数据：' + s


class JsonConstantFormatException(JsonFormatException):
    def __init__(self, s):
        self.message = '常量请用false, true, none格式，当前错误数据：' + s



