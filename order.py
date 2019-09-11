#!/usr/bin/env python3

from common import JSONSerialized


class Order(JSONSerialized):
    '''
    Represents a group of metal purchases.
    '''
    @staticmethod
    def set_price_data(price_data):
        OrderContents.price_data = price_data

    @staticmethod
    def set_assets(assets):
        OrderContents.assets = assets

    @classmethod
    def from_dict(cls, dict_in):
        # Adjust json contents (list) to obj list
        dict_in['content'] = OrderContents.from_list_dict(dict_in['content'])
        return cls(**dict_in)

    def __init__(self, content):
        self.content = content

class OrderContents(JSONSerialized):
    '''
    Represents a single asset being purchased within an order.
    '''
    def __init__(self, asset, quantity, rate):
        self.asset = asset
        self.quantity = quantity
        self.rate = rate


if __name__ == '__main__':
    pass
