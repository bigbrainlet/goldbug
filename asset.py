#!/usr/bin/env python3

from decimal import Decimal

from common import JSONSerialized


class Asset(JSONSerialized):
    G_TO_TROY_OZ = Decimal(0.0321507)

    @staticmethod
    def to_dict(asset_list):
        return dict([(asset.token, asset) for asset in asset_list])

    @staticmethod
    def to_list(asset_dict):
        return list(asset_dict.values())

    def __init__(self, token, composition, mass, desc=''):
        self.token = token
        self.composition = dict(
                [(comp, Decimal(purity)) for comp, purity in composition.items()])
        self.mass = Decimal(mass)
        self.weight = self.mass * self.__class__.G_TO_TROY_OZ
        self.desc = desc


if __name__ == '__main__':
    pass
