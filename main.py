#!/usr/bin/env python3

import glob
import json
import os
import re

import requests


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

    order_files = glob.glob('{}/*.json'.format(filepaths['order_dir']))
    data_files = glob.glob('{}/*.json'.format(filepaths['data_dir']))

    data = {}
    for data_file in data_files:
        # Flatten data from all files into single dict
        with open(data_file, 'r') as f:
            to_add = json.load(f)
            for key, value in to_add.items():
                data[key] = value
    
    order_file_obj = [open(order_file, 'r') for order_file in order_files]
    orders = [json.load(file_obj) for file_obj in order_file_obj]
    [file_obj.close() for file_obj in order_file_obj]

    # Process orders
    print('{} order(s) in system'.format(len(orders)))
    account_value = sum([order_value(price_data, data, order) for order in orders])

    print('Total account value (current spot price): ${}'.format(account_value))


def order_value(price_data, data_dict, order):
    '''
    Returns the float USD value of an order based on current spot price.
    '''
    return sum([content_value(price_data, data_dict, content)
        for content in order['contents']])

def content_value(price_data, data_dict, content):
    '''
    Return the float USD value of a specific content of an order.
    '''
    name = content['type']
    metal = content.get('metal', data_dict[name]['metals'][0])
    price_oz = price_data[metal]
    purity = data_dict[name]['purity']
    weight = content['quantity'] * data_dict[name]['weight']
    return price_oz * purity * weight


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
