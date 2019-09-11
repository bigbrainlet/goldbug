#!/usr/bin/env python3

from common import JSONSerialized


class Asset(JSONSerialized):
    @staticmethod
    def to_dict(asset_list):
        return dict([(asset.token, asset) for asset in asset_list])

    @staticmethod
    def to_list(asset_dict):
        return list(asset_dict.values())

    def __init__(self, token, metal, purity, weight, desc=''):
        self.token = token
        self.metal = metal
        self.purity = purity
        self.weight = weight
        self.desc = desc


if __name__ == '__main__':
    pass
