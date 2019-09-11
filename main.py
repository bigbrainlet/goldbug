#!/usr/bin/env python3

import glob
import json
import os
import re

import requests

from asset import Asset
from order import Order
from common import list_sum


filepaths = {
        'config': 'config.json',
        'order_dir': 'orders',
        'data_dir': 'data',
        }


def main():
    with open(filepaths['config'], 'r') as f:
        config = json.load(f)
    price_data = {}
    if config['price_data']['enabled']:
        price_data = get_price_data(config['metals'], config['price_data']['sources'])
    print('Current prices (USD/oz)')
    for metal in config['metals']:
        print('{}: {}'.format(metal, price_data.get(metal, 'N/A')))

    asset_files = glob.glob('{}/*.json'.format(filepaths['data_dir']))
    order_files = glob.glob('{}/*.json'.format(filepaths['order_dir']))

    assets = list_sum(
            [Asset.from_json_list_file(asset_file) for asset_file in asset_files])
    assets = Asset.to_dict(assets)
    orders = list_sum(
            [Order.from_json_list_file(order_file) for order_file in order_files])

    Order.set_price_data(price_data)
    Order.set_assets(assets)

    account_value = round(sum([order.value() for order in orders]), 2)
    print('Total account value: ${}'.format(account_value))

    metal_holdings = dict(
            [(metal, sum([order.quantity(metal) for order in orders]))
                for metal in config['metals']])
    print('Metal holdings:')
    for metal in config['metals']:
        print('{}: {}oz'.format(metal, metal_holdings[metal]))


def get_price_data(metals, sources):
    '''
    Retrieves price data for metals from url with regex patterns.
    '''
    for source, source_dict in sources.items():
        price_data = {}
        print('Retrieving price data from {}'.format(source))
        session = requests.get(source_dict['url'])
        for metal in metals:
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
                price_data[metal] = float(spot)
            elif bid and ask:
                price_data[metal] = (float(bid)+float(ask))/2
            else:
                print('Unable to retrieve price data for {} from {}'.format(metal, source))
                break
        if len(price_data.keys()) == len(metals):
            return price_data
    return {}



if __name__ == '__main__':
    main()
