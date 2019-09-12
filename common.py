#!/usr/bin/env python3

from decimal import Decimal
import json


def list_sum(lists):
    '''
    Return a flattened list from many list inputs.
    '''
    ret = []
    for each in lists:
        ret.extend(each)
    return ret


class JSONSerialized:
    dump_kwargs = {
            'sort_keys': True,
            'indent': 2,
            }

    @classmethod
    def from_json_list_file(cls, filename):
        with open(filename, 'r') as f:
            return cls.from_list_dict(json.load(f))

    @classmethod
    def from_json_dict_file(cls, filename):
        with open(filename, 'r') as f:
            return cls.from_dict(json.load(f))

    @classmethod
    def from_list_dict(cls, list_dict):
        return [cls.from_dict(each) for each in list_dict]

    @classmethod
    def from_dict(cls, dict_in):
        return cls(**dict_in)

    def to_dict(self):
        attrs = self.__class__.json_attrs
        data = [(attr, getattr(self, attr)) for attr in attrs]
        return dict(data)


if __name__ == '__main__':
    pass
