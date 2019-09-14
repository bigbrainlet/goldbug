#!/usr/bin/env python3

from decimal import Decimal
import json
import re
import time

import requests

from common import JSONSerialized


class PriceCache(JSONSerialized):
    filename = '.cache.json'
    json_attrs = ['updated', 'price_data']
    config = {}

    @classmethod
    def read(cls):
        try:
            with open(cls.filename, 'r') as f:
                return cls.from_dict(json.load(f))
        except FileNotFoundError:
            return cls(0, {})

    def write(self):
        with open(self.__class__.filename, 'w') as f:
            to_write = self.to_dict()
            to_write['price_data'] = dict(
                    [(key, str(value)) for key, value in to_write['price_data'].items()])
            json.dump(to_write, f, **self.__class__.dump_kwargs)

    def __init__(self, updated, price_data):
        self.updated = updated
        self.price_data = dict(
                [(metal, Decimal(price)) for metal, price in price_data.items()])
        if (not self.price_data or
                abs(time.time() - updated) > self.__class__.config['cache_update']):
            self.generate()
            self.write()

    def generate(self):
        '''
        Retrieve and set new price data.
        '''
        self.updated = time.time()
        self.get_price_data()

    def get_price_data(self):
        '''
        Retrieves price data for metals from url with regex patterns.
        '''
        for source, source_dict in self.__class__.config['price_data']['sources'].items():
            price_data = {}
            print('Retrieving price data from {}'.format(source))
            session = requests.get(source_dict['url'])
            for metal in self.config['metals']:
                symbol = source_dict['symbol'].get(metal, metal)
                pattern = source_dict['regex'].get(metal, source_dict['regex']['default'])
                pattern = pattern.format(symbol)
                # Perform a case-insensitive search for this metals price in the webpage
                # Prefer specific regex for this metal, fallback to 'default'
                match = re.search(pattern, session.text, re.I|re.DOTALL)
                try:
                    spot = match.group('spot')
                except IndexError:
                    spot = None
                try:
                    bid = match.group('bid')
                    ask = match.group('ask')
                except IndexError:
                    bid = ask = None
    
                if spot:
                    price_data[metal] = Decimal(spot)
                elif bid and ask:
                    price_data[metal] = (Decimal(bid)+Decimal(ask))/2
                else:
                    print('Unable to retrieve price data for {} from {}'.format(metal, source))
                    break
            if len(price_data.keys()) == len(self.__class__.config['metals']):
                self.price_data = dict(
                        [(metal, Decimal(price)) for metal, price in price_data.items()])


if __name__ == '__main__':
    pass
