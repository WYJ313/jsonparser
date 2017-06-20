#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jsonexcept import JsonStringFormatException, JsonListFormatException, JsonDictFormatException,\
    JsonNumberFormatException, JsonConstantFormatException, JsonFormatException

import logging


class JsonParser:
    def __init__(self):
        self._data = {}

    def _parse_string(self, s):  # 传入"..."字符串
        s = s.strip().strip(',').strip()
        if s[0] == '\"' and s[-1] == '\"':
            return s.strip('\"')
        else:
            raise JsonStringFormatException(s)

    def _parse_number(self, s):
        s = s.strip().strip(',').strip()
        if ((s[0] >= '0' and s[0] <= '9') or s[0] == '-') and (s[-1] >= '0' and s[-1] <= '9') and s.count('.') <= 1:
            if s.find('.') != -1:
                return float(s)
            else:
                return int(s)
        else:
            raise JsonNumberFormatException(s)

    def _parse_list(self, s):  # 传入[...]字符串
        s = s.strip().strip(',').strip()
        if s[0] == '[' and s[-1] == ']':
            s = s[1:-1]  # 除去[]
            res = []
            # print(s)
            while s is not None:
                s = s.strip().strip(',').strip()  # 去除空格及逗号
                if s[0] == '"':
                    end = s.find('"', 1)  # end代表"的下标
                    # print(s[:end+1])
                    res.append(self._parse_string(s[:end + 1]))
                    if end + 1 <= len(s) - 1:
                        s = s[end + 1:]  # 从"后开始
                    else:
                        break
                elif s[0] == '[':
                    tmp = []
                    flag = 0
                    for i in range(len(s)):
                        if s[i] == '[':
                            flag += 1
                        elif s[i] == ']':
                            flag -= 1
                        elif flag == 0:
                            break  # i代表]的下标
                    tmp = self._parse_list(s[:i + 1])
                    res.append(tmp)
                    if i + 1 <= len(s) - 1:  # 从]后开始
                        s = s[i + 1:]
                    else:
                        break
                elif s[0] == '{':
                    flag = 0
                    for i in range(len(s)):
                        if s[i] == '{':
                            flag += 1
                        elif s[i] == '}':
                            flag -= 1
                        elif flag == 0:
                            break               # i代表]的下标
                    res.append(self._parse_dict(s[:i + 1]))
                    if i + 1 <= len(s) - 1:     # 从}开始
                        s = s[i + 1:]
                    else:
                        break
                elif s[0] == 't':
                    if s[:4] == 'true':
                        res.append(True)
                        end = 3
                        if end + 1 <= len(s) - 1:
                            s = s[end + 1:]
                        else:
                            break
                    else:
                        raise JsonConstantFormatException(s)
                elif s[0] == 'f':
                    if s[:5] == 'false':
                        res.append(False)
                        end = 4
                        if end + 1 <= len(s) - 1:
                            s = s[end + 1:]
                        else:
                            break
                    else:
                        raise JsonConstantFormatException(s)
                elif s[0] == 'n':
                    if s[0:4] == 'none':
                        res.append(None)
                        end = 3
                        if end + 1 <= len(s) - 1:
                            s = s[end + 1:]
                        else:
                            break
                    else:
                        raise JsonConstantFormatException(s)
                elif s[0] == '-' or (s[0] >= '0' and s[0] <= '9'):
                    dotcount = 0
                    end = 1
                    while(end <= len(s)-1):
                        if s[end] >='0' and s[end] <= '9':
                            end += 1
                        elif s[end] == '.':
                            if dotcount > 1:
                                raise JsonNumberFormatException(s)
                            else:
                                dotcount += 1
                        else:
                            break
                    res.append(self._parse_number(s[:end]))
                    if end + 1 <= len(s) - 1:
                        s = s[end + 1:]
                    else:
                        break
                else:
                    #continue
                    raise JsonFormatException(s)
            return res
        else:
            raise JsonListFormatException(s)

    def _parse_dict(self, s):  # 传入{...}字符串
        s = s.strip().strip(',').strip()
        if s[0] == '{' and s[-1] == '}':
            s = s[1:-1]
            res = {}
            while s is not None:
                s = s.strip().strip(',').strip()
                i = s.find(':')
                key = self._parse_string(s[:i]).strip()
                # print(key)
                s = s[i + 1:].strip()
                if s[0] == '"':
                    end = s.find('"', 1)  # end代表”的下标
                    # print(s[:end+1])
                    res[key] = self._parse_string(s[:end + 1])
                    if end + 1 <= len(s) - 1:
                        s = s[end + 1:]  # 在”后空一位再开始
                    else:
                        break
                elif s[0] == '[':
                    flag = 0
                    for i in range(len(s)):
                        if s[i] == '[':
                            flag += 1
                        elif s[i] == ']':
                            flag -= 1
                        elif flag == 0:
                            break  # i代表]的下标
                    res[key] = self._parse_list(s[:i + 1])
                    if i + 1 <= len(s) - 1:  # 在]后空一位再开始
                        s = s[i + 1:]
                    else:
                        break
                elif s[0] == '{':
                    flag = 0
                    for i in range(len(s)):
                        if s[i] == '{':
                            flag += 1
                        elif s[i] == '}':
                            flag -= 1
                        elif flag == 0:
                            break  # i代表]的下标
                    res[key] = self._parse_dict(s[:i + 1])
                    if i + 1 <= len(s) - 1:  # 在]后空一位再开始
                        s = s[i + 1:]
                    else:
                        break
                elif s[0] == 't':
                    if s[:4] == 'true':
                        res[key] = True
                        end = 3
                        if end + 1 <= len(s) - 1:
                            s = s[end + 1:]
                        else:
                            break
                    else:
                        raise JsonConstantFormatException
                elif s[0] == 'f':
                    if s[:5] == 'false':
                        res[key] = False
                        end = 4
                        if end + 1 <= len(s) - 1:
                            s = s[end + 1:]
                        else:
                            break
                    else:
                        raise JsonConstantFormatException
                elif s[0] == 'n':
                    if s[0:4] == 'none':
                        res[key] = None
                        end = 3
                        if end + 1 <= len(s) - 1:
                            s = s[end + 1:]
                        else:
                            break
                    else:
                        raise JsonConstantFormatException
                elif s[0] == '-' or (s[0] >= '0' and s[0] <= '9'):
                    dotcount = 0
                    end = 1
                    while end <= len(s)-1:
                        if s[end] >='0' and s[end] <= '9':
                            end += 1
                        elif s[end] == '.':
                            if dotcount > 1:
                                break
                            else:
                                end += 1
                                dotcount += 1
                        else:
                            break
                    res[key] = self._parse_number(s[:end])
                    if end + 1 <= len(s) - 1:
                        s = s[end + 1:]
                    else:
                        break
                else:
                    raise JsonFormatException(s)
            return res
        else:
            raise JsonDictFormatException(s)

    def _string_to_string(self, s):
        return '"'+s+'"'

    def _list_to_string(self, List):
        s = '['
        if List is None:
            return None
        if len(List) == 0:
            return '[]'
        for i in range(len(List)):
            if type(List[i]) == str:
                s += self._string_to_string(List[i])
            elif type(List[i]) == list:
                s += self._list_to_string(List[i])
            elif type(List[i]) == dict:
                s += self._dict_to_string(List[i])
            elif List[i] is True or List[i] is False or List[i] is None:
                s += str(List[i]).lower()
            elif isinstance(List[i], float) or isinstance(List[i], int):
                s += str(List[i])
            if i == len(List)-1:
                s += ']'
            else:
                s += ', '
        return s

    def _dict_to_string(self, Dict):
        s = '{'
        count = 0
        if Dict is None:
            return None
        if len(Dict) == 0:
            return '{}'
        for key in Dict.keys():
            s += self._string_to_string(key) + ': '
            if type(Dict[key]) == str:
                s += self._string_to_string(Dict[key])
            elif type(Dict[key]) == list:
                s += self._list_to_string(Dict[key])
            elif type(Dict[key]) == dict:
                s += self._dict_to_string(Dict[key])
            elif Dict[key] is True or Dict[key] is False or Dict[key] is None:
                s += str(Dict[key]).lower()
            elif isinstance(Dict[key], float) or isinstance(Dict[key], int):
                s += str(Dict[key])
            count += 1
            if count == len(Dict):
                s += '}'
            else:
                s += ', '
        return s

    def load(self, s):
        s = s.replace('\n', '').replace('\r', '').replace('\t', '').replace('\b', '').replace('\f', '')
        try:
            self._data = self._parse_dict(s)
        except (JsonFormatException, JsonNumberFormatException, JsonConstantFormatException, JsonDictFormatException,
                JsonStringFormatException) as e:
            logging.exception(e.message)
            raise e

    def dump(self):
        return self._dict_to_string(self._data)

    def load_file(self, f):
        try:
            try:
                input = open(f, 'r')
                self.load(input.read())
                input.close()
            except IOError:
                raise IOError("读取Json文件失败")
        except IOError as e:
            logging.error(e.message)

    def dump_file(self, f):
        try:
            try:
                output = open(f, 'w')
                output.write(self.dump())
                output.close()
            except IOError:
                raise IOError('写入Json文件失败')
        except IOError as e:
            logging.error(e)

    def _deepcopy_list(self, List):
        if type(List) == list:
            res = []
            for i in List:
                if type(i) == str:
                    res.append(i)
                elif type(i) == list:
                    res.append(self._deepcopy_list(i))
                elif type(i) == dict:
                    res.append(self._deepcopy_dict(i))
                elif i is True or i is False or i is None:
                    res.append(i)
                elif isinstance(i, float) or isinstance(i, int):
                    res.append(i)
                else:
                    ValueError('无法识别的对象类型')
            return res
        else:
            raise ValueError("参数错误：请传入list对象")

    def _deepcopy_dict(self, d):
        if type(d) == dict:
            res = {}
            for key in d.keys():
                if type(key) == str:
                    if type(d[key]) == str:
                        res[key] = d[key]
                    elif type(d[key]) == list:
                        res[key] = self._deepcopy_list(d[key])
                    elif type(d[key]) == dict:
                        res[key] = self._deepcopy_dict(d[key])
                    elif d[key] is True or d[key] is False or d[key] is None:
                        res[key] = d[key]
                    elif isinstance(d[key], float) or isinstance(d[key], int):
                        res[key] = d[key]
                    else:
                        raise ValueError('无法识别的对象类型')
            return res
        else:
            raise ValueError("参数错误：请传入dict对象")

    def load_dict(self, d):
        try:
            self._data = self._deepcopy_dict(d)
        except ValueError as e:
            logging.error(e)

    def dump_dict(self):
        try:
            return self._deepcopy_dict(self._data)
        except ValueError as e:
            logging.error(e.message)

    def __getitem__(self, item):
        try:
            try:
                return self._data[item]
            except KeyError:
                raise KeyError('当前Json对象不存在名为"'+item+'"的键')
        except KeyError as e:
            logging.error(e.message)

    def __setitem__(self, key, v):
        try:
            if type(key) == str:
                if type(v) == list or type(v) == dict or v is True or v is False or v is None \
                        or type(v) == int or type(v) == float:
                    self._data[key] = v
                else:
                    raise ValueError('设置Json对象的值类型无法识别')
            else:
                raise KeyError('设置Json对象的键必须为字符串')
        except (KeyError, ValueError) as e:
            logging.error(e.message)

    def update(self, d):
        for key in d.keys():
            self._data[key] = d[key]


if __name__ == '__main__':
    testD = '{"as":"as", "bs":["bs","bs"], "cs":{"ds":"ds"}}'
    testD = '''
    {
"name":"Bill Gates",
"street":"Fifth Avenue New York 666",
"age":56,
"phone":"555 1234567"}
    '''
    #print(testD)
    js = JsonParser()
    js.load(testD)
    #print(js._data)
    print(type(js['age']) )
    print(js['age'] is int)
    print(isinstance(js['age'], int))
    print(js._data)
    print(js.dump())
    testD = '{"a":"a", "b":["b","b"], "c":{"d":"d"}}'
    testD = '''
    {
"employees": [
{ "firstName":"John" , "lastName":"Doe" },
{ "firstName":"Anna" , "lastName":"Smith" },
{ "firstName":"Peter" , "lastName":"Jones" }
]
}
    '''
    js.load(testD)
    #print(js._data)
    print(js.dump())
    #print(js['a'])
    #js['a'] = 'sss'
    #print(js['a'])
    input = './testin'
    js.load_file(input)
    output = './testout'
    js.dump_file(output)
    testT = '{"as": true, "bs": [true, true], "cs": {"ds": true}}'
    js.load(testT)
    #print(js._data)
    print(js.dump())
    testT = '{"as": false "bs": [false, false], "cs": {"ds": false}}'
    js.load(testT)
    #print(js._data)
    print(js.dump())
    testT = '{"as": none, "bs": [none, none], "cs": {"ds": none}}'
    js.load(testT)
    #print(js._data)
    print(js.dump())
    testI = '{"a": 12.34, "b": [-250, 250]}'
    js.load(testI)
    print(js._data)
    #testL = [[1, 2], [3, 4]]
    #js.load_dict(testL)
    print(js['c'])


