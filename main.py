#!/usr/bin/env python3

import glob
import json
import os

from asset import Asset
from order import Order, Account
from price import PriceCache
from common import list_sum


filepaths = {
        'config': 'config.json',
        'order_dir': 'orders',
        'data_dir': 'data',
        }

def main():
    with open(filepaths['config'], 'r') as f:
        config = json.load(f)

    PriceCache.config = config
    price_cache = PriceCache.read()

    asset_dir = os.path.join(filepaths['data_dir'], '*.json')
    order_dir = os.path.join(filepaths['order_dir'], '*.json')
    asset_files = glob.glob(asset_dir)
    order_files = glob.glob(order_dir)

    assets = list_sum(
            [Asset.from_json_list_file(asset_file) for asset_file in asset_files])
    assets = Asset.to_dict(assets)
    orders = list_sum(
            [Order.from_json_list_file(order_file) for order_file in order_files])

    Order.set_price_data(price_cache.price_data)
    Order.set_assets(assets)

    account = Account(orders, assets)
    account.print_summary()


if __name__ == '__main__':
    main()
