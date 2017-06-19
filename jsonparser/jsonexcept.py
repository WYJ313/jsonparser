#!/usr/bin/env python
# -*- coding: utf-8 -*-


class JsonException(Exception):
    pass


class JsonFormatException(JsonException):
    def __init__(self, s):
        self._message = s

    def info(self):
        return 'JsonFormatException: 未知格式错误，当前错误数据：'+self._message


class JsonStringFormatException(JsonFormatException):
    def __init__(self, s):
        self._message = s

    def info(self):
        return 'JsonStringFormatException: 字符串请用"xx"格式，当前错误数据：'+self._message


class JsonListFormatException(JsonFormatException):
    def __init__(self, s):
        self._message = s

    def info(self):
        return 'JsonListFormatException: 列表请用[xx, ...]格式，当前错误数据：'+self._message


class JsonDictFormatException(JsonFormatException):
    def __init__(self, s):
        self._message = s

    def info(self):
        return 'JsonListFormatException: 字典请用{xx: xxx, ...}格式，当前错误数据：'+self._message


class JsonNumberFormatException(JsonFormatException):
    def __init__(self, s):
        self._message = s

    def info(self):
        return 'JsonNumberFormatException: 数字请用xx, -xx, xx.xx格式，当前错误数据：'+self._message


class JsonConstantFormatException(JsonFormatException):
    def __init__(self, s):
        self._message = s

    def info(self):
        return 'JsonConstantFormatException: 常量请用false, true, none格式，当前错误数据：'+self._message


class JsonFileException(JsonException):
    pass


class JsonFileLoadException(JsonFileException):
    def info(self):
        return 'JsonFileLoadException: 没有找到Json文件或读取文件失败'


class JsonFileDumpException(JsonFileException):
    def info(self):
        return 'JsonFileDumpException: 写入Json文件失败'
