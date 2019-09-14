#!/usr/bin/env python3

from decimal import Decimal, InvalidOperation
import json
import unittest


class JSONifyDecimal:
    '''
    Serialized data class (JSON format) that uses 
    Decimal module in place of floats, storing them as strings
    in JSON.
    '''
    json_kwargs = {
            'sort_keys': True,
            'indent': 2,
            }

    @classmethod
    def read(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        if type(data) is list:
            return cls.from_list(data)
        elif type(data) is dict:
            return cls.from_dict(data)
        else:
            raise ValueError('Invalid {} in JSON file {}'.format(
                cls, filename))

    @classmethod
    def write(cls, filename, obj_list):
        with open(filename, 'w') as f:
            json.dump(cls.to_list(obj_list), f, **cls.json_kwargs)

    @classmethod
    def from_list(cls, list_in):
        return [cls.from_dict(each) for each in list_in]

    @classmethod
    def to_list(cls, list_in):
        return [each.to_dict() for each in list_in]

    @classmethod
    def from_dict(cls, dict_in):
        return cls(**rec_str_to_dec(dict_in))

    def to_dict(self):
        return rec_dec_to_str(dict(
            [(attr, getattr(self, attr)) for
                attr in self.__class__.json_attrs]))


def rec_dec_to_str(data_in):
    '''
    Recurse down data structure looking for decimals to convert to
    strings.
    '''
    data_type = type(data_in)
    if data_type is Decimal:
        return str(data_in)
    elif data_type is list:
        return [rec_dec_to_str(each) for each in data_in]
    elif data_type is dict:
        return dict(
                [(rec_dec_to_str(key), rec_dec_to_str(value)) for
                    key, value in data_in.items()])
    return data_in


def rec_str_to_dec(data_in):
    '''
    Recurse down a data structure (lists, dicts) and 
    convert all strings to decimal.
    '''
    data_type = type(data_in)
    if data_type is str:
        try:
            return Decimal(data_in)
        except InvalidOperation:
            # Non-decimal string
            return data_in
    elif data_type is int:
        return Decimal(data_in)
    elif data_type is float:
        return Decimal(data_in)
    elif data_type is list:
        return [rec_str_to_dec(each) for each in data_in]
    elif data_type is dict:
        return dict(
                [(rec_str_to_dec(key), rec_str_to_dec(value)) for
                    key, value in data_in.items()])
    return data_in


class ObjTest(JSONifyDecimal):
    json_attrs = ['name', 'date', 'color']

    def __init__(self, name, date, color):
        self.name = name
        self.date = date
        self.color = color


class TestListOfObj(unittest.TestCase):
    def setUp(self):
        self.test_list = [
                {
                    'name': 'hello',
                    'date': '123.434234',
                    'color': {
                        'green': '98.63000',
                        },
                    },
                {
                    'name': 'world',
                    'date': '10043.2736',
                    'color': {
                        'red': '09.64532',
                        },
                    },
                ]

    def test_from_list(self):
        list_res = ObjTest.from_list(self.test_list)
        for each in list_res:
            self.assertEqual(type(each), ObjTest)
            self.assertEqual(type(each.date), Decimal)
            self.assertEqual(type(each.color), dict)

    def test_list_write(self):
        list_res = ObjTest.from_list(self.test_list)
        ObjTest.write('test.json', list_res)
        ObjTest.read('test.json')

    def test_invalid_file(self):
        self.assertRaises(ValueError, ObjTest.read, 'invalid.json')


if __name__ == '__main__':
    unittest.main()
