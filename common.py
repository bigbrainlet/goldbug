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


if __name__ == '__main__':
    pass
