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

    def __init__(self, content, tax=0.0, ship=0.0):
        self.content = content
        self.tax = tax
        self.ship = ship

    def cost(self):
        return round(
                sum(
                    [content.cost() for content in self.content]) +
                self.tax +
                self.ship,
                2)

    def value(self):
        '''
        Return total value (USD) of order.
        '''
        return round(sum([content.value() for content in self.content]), 2)

    def quantity(self, metal):
        '''
        Return the total quantity of given metal in this order.
        '''
        return round(sum([each.metal_content(metal) for each in self.content]), 4)

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
        return (sum(
                [self.__class__.price_data.get(metal, 0) * purity for
                    metal, purity in asset.composition.items()]) *
                asset.weight * self.quantity)

    def cost(self):
        return self.rate * self.quantity

    def metal_content(self, metal):
        '''
        Return the total (pure) metal in oz.
        '''
        asset = self.get_asset()
        return asset.composition.get(metal, 0) * asset.weight * self.quantity

    def get_asset(self):
        return self.__class__.assets[self.asset]


if __name__ == '__main__':
    pass
