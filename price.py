#!/usr/bin/env python3

from common import JSONSerialized


class PriceCache(JSONSerialized):
    filename = '.cache.json'
    json_attrs = ['updated', 'price_data']

    def __init__(self, updated, price_data):
        self.updated = updated
        self.price_data = price_data


if __name__ == '__main__':
    pass
