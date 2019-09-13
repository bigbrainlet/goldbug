#!/usr/bin/env python3

from decimal import Decimal

from common import JSONSerialized


class Account:
    '''
    Manages a group of orders.
    '''
    QUANTITY_ROUND = 4
    PRICE_ROUND = 2

    sep_str = '=' * 28
    label_fmt = '{0: <12}'
    number_fmt = '{1: >12}'
    amt_fmt = ']  {}:{}'

    @classmethod
    def set_price_data(cls, price_data):
        cls.price_data = price_data
        Order.set_price_data(cls.price_data)

    @classmethod
    def set_config(cls, config):
        cls.config = config

    def __init__(self, orders, assets):
        self.orders = orders
        self.assets = assets

    def print_summary(self):
        '''
        Print a pretty account summary.
        '''
        sep = self.__class__.sep_str
        fmt = self.__class__.amt_fmt.format(
                self.__class__.label_fmt,
                self.__class__.number_fmt)
        cost = self.cost()
        value = self.value()
        profit = value - cost
        if profit < 0:
            profit = '({})'.format(abs(profit))
            if len(profit) < 13:
                profit = ' ' * (13-len(profit)) + profit
        to_print = [
                sep,
                ' Account Total (USD)',
                fmt.format('investment', cost),
                fmt.format('value', value),
                fmt.format('profit', profit),
                sep,
                ' Holdings (Troy oz)',
                *[fmt.format(metal, self.holding(metal))
                    for metal in self.__class__.config['metals']],
                sep,
                ' Price Data (USD/Troy oz)',
                *[fmt.format(metal,
                    round(self.__class__.price_data.get(metal, 0),
                        self.__class__.PRICE_ROUND))
                    for metal in
                    self.__class__.price_data],
                sep,]
        print('\n'.join(to_print))

    def holding(self, metal):
        '''
        Return the quantity of a metal being held.
        '''
        return round(sum([order.quantity(metal) for order in self.orders]),
                self.__class__.QUANTITY_ROUND)

    def cost(self):
        return round(sum([order.cost() for order in self.orders]),
                self.__class__.PRICE_ROUND)

    def value(self):
        return round(sum([order.value() for order in self.orders]),
                self.__class__.PRICE_ROUND)


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
        self.tax = Decimal(tax)
        self.ship = Decimal(ship)

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
        self.quantity = Decimal(quantity)
        self.rate = Decimal(rate)

    def value(self):
        '''
        Return value of contents based on current spot price.
        '''
        asset = self.get_asset()
        return (sum(
                [self.__class__.price_data.get(metal, Decimal(0.0)) * purity for
                    metal, purity in asset.composition.items()]) *
                asset.weight * self.quantity)

    def cost(self):
        return self.rate * self.quantity

    def metal_content(self, metal):
        '''
        Return the total (pure) metal in oz.
        '''
        asset = self.get_asset()
        return asset.composition.get(metal, Decimal(0.0)) * asset.weight * self.quantity

    def get_asset(self):
        return self.__class__.assets[self.asset]


if __name__ == '__main__':
    pass
