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

    def value(self):
        '''
        Return total value (USD) of order.
        '''
        return sum([content.value() for content in self.content])

    def quantity(self, metal):
        '''
        Return the total quantity of given metal in this order.
        '''
        applicable = [content for content in self.content if
                content.get_asset().metal == metal]
        return sum([each.metal_content() for each in applicable])

class OrderContents(JSONSerialized):
    '''
    Represents a single asset being purchased within an order.
    '''
    def __init__(self, asset, quantity, rate):
        self.asset = asset
        self.quantity = quantity
        self.rate = rate

    def value(self):
        '''
        Return value of contents based on current spot price.
        '''
        asset = self.get_asset()
        return (
                self.__class__.price_data[asset.metal] *
                asset.purity *
                asset.weight *
                self.quantity)

    def metal_content(self):
        '''
        Return the total (pure) metal in oz.
        '''
        asset = self.get_asset()
        return asset.weight * self.quantity

    def get_asset(self):
        return self.__class__.assets[self.asset]


if __name__ == '__main__':
    pass
