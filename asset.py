#!/usr/bin/env python3

from decimal import Decimal

from decimal_json import JSONifyDecimal


class Asset(JSONifyDecimal):
    G_TO_TROY_OZ = Decimal(0.0321507)

    def __init__(self, token, composition, mass, desc=''):
        self.token = token
        self.composition = dict(
                [(comp, Decimal(purity)) for comp, purity in composition.items()])
        self.mass = Decimal(mass)
        self.weight = self.mass * self.__class__.G_TO_TROY_OZ
        self.desc = desc


if __name__ == '__main__':
    pass
