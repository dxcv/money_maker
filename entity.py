#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os


def handle_deque(deq, entity, ts, ind):
    while len(deq) > 0:
        left = deq.popleft()
        if float(left.time + ind.interval) > float(ts):
            deq.appendleft(left)
            break
        ind.minus_vol(left)
        ind.minus_price(left)
    deq.append(entity)
    ind.add_price(entity)
    ind.add_vol(entity)


class Coin:
    def __init__(self, name, refer):
        self.name = name
        self.refer = refer

    def gen_file_name(self):
        file_path = os.getcwd()
        transaction = file_path + '/' + self.name + '_transaction.txt'
        deal = file_path + '/' + self.name + '_deals.txt'
        return transaction, deal

    def gen_future_file_name(self):
        file_path = os.getcwd()
        transaction = file_path + '/' + self.name + '_future_transaction.txt'
        deal = file_path + '/' + self.name + '_future_deals.txt'
        return transaction, deal

    def gen_full_name(self):
        return self.name + "_" + self.refer

    def get_depth_filename(self):
        file_path = os.getcwd()
        depth = file_path + '/' + self.name + '_future_depth.txt'
        return depth


class IndexEntity:
    def __init__(self, _coin_name, _index, _timestamp):
        self.coin_name = _coin_name
        self.index = _index
        self.timestamp = _timestamp


class IndexIndicator:
    def __init__(self, coin_name, interval):
        self.coin_name = coin_name
        self.interval = interval
        self.index = 0
        self.index_num = 0

    def add_index(self, index_entity):
        self.index += index_entity.index
        self.index_num += 1

    def minus_index(self, index_entity):
        self.index -= index_entity.index
        self.index_num -= 1

    def cal_avg_price(self):
        if self.index_num != 0:
            return round(float(self.index) / float(self.index_num), 4)
        else:
            return 0


class DealEntity:
    def __init__(self, _id, _price, _amount, _time, _type):
        self.id = _id
        self.price = _price
        self.amount = _amount
        self.time = _time
        self.type = _type

    def detail(self):
        if self.type == 'ask':
            category = 'sell '
        else:
            category = 'buy  '
        return str(self.time) + ': ' + category + str(self.amount) + '\t at price: ' + str(self.price)


class Indicator:
    def __init__(self, interval):
        self.interval = interval
        self.vol = 0
        self.avg_price = 0
        self.price = 0
        self.price_num = 0
        self.bid_vol = 0
        self.ask_vol = 0

    def cal_avg_price(self):
        if self.price_num != 0:
            return round(float(self.price) / float(self.price_num), 4)
        else:
            return 0

    def add_vol(self, deal_entity):
        self.vol += deal_entity.amount
        if deal_entity.type == 'ask':
            self.ask_vol += deal_entity.amount
        elif deal_entity.type == 'bid':
            self.bid_vol += deal_entity.amount

    def minus_vol(self, deal_entity):
        self.vol -= deal_entity.amount
        if deal_entity.type == 'ask':
            self.ask_vol -= deal_entity.amount
        elif deal_entity.type == 'bid':
            self.bid_vol -= deal_entity.amount

    def add_price(self, deal_entity):
        self.price_num += 1
        self.price += deal_entity.price

    def minus_price(self, deal_entity):
        self.price_num -= 1
        self.price -= deal_entity.price