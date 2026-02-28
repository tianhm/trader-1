# coding=utf-8
#
# Copyright 2016 timercrack
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from django.db import models


class ContractType(models.TextChoices):
    STOCK = 'STOCK', '股票'
    FUTURE = 'FUTURE', '期货'
    OPTION = 'OPTION', '期权'


class ExchangeType(models.TextChoices):
    SHFE = 'SHFE', '上期所'
    DCE = 'DCE', '大商所'
    CZCE = 'CZCE', '郑商所'
    CFFEX = 'CFFEX', '中金所'
    INE = 'INE', '上期能源'
    GFEX = 'GFEX', '广交所'


class SectionType(models.TextChoices):
    Financial = '金融', '金融'
    PreciousMetal = '贵金属', '贵金属'
    BaseMetal = '有色金属', '有色金属'
    Ferrous = '黑色产业', '黑色产业'
    Energy = '能源', '能源'
    Chemical = '化工', '化工'
    Agriculture = '农牧', '农牧'
    NewEnergy = '新能源', '新能源'


class SortType(models.TextChoices):
    StockIndex = '股指', '股指'
    Treasury = '国债', '国债'
    Shipping = '航运', '航运'
    Precious = '贵金属', '贵金属'
    CopperChain = '铜产业链', '铜产业链'
    AluminumChain = '铝产业链', '铝产业链'
    OtherNonferrous = '其他有色', '其他有色'
    SteelChain = '钢铁链', '钢铁链'
    BuildMaterial = '建材', '建材'
    CrudeOilChain = '原油链', '原油链'
    Olefin = '烯烃', '烯烃'
    Aromatic = '芳烃', '芳烃'
    Rubber = '橡胶', '橡胶'
    CoalChem = '煤化工', '煤化工'
    OilFat = '油脂油料', '油脂油料'
    GrainFeed = '谷物饲料', '谷物饲料'
    SoftAgri = '软商品', '软商品'
    Livestock = '畜牧', '畜牧'
    Forestry = '林纸', '林纸'
    NewEnergyMat = '新能源材料', '新能源材料'


class AddressType(models.TextChoices):
    TRADE = 'TRADE', '交易'
    MARKET = 'MARKET', '行情'


class OperatorType(models.TextChoices):
    TELECOM = 'TELECOM', '电信'
    UNICOM = 'UNICOM', '联通'


class DirectionType(models.TextChoices):
    LONG = '0', '多'
    SHORT = '1', '空'


class CombOffsetFlag(models.TextChoices):  # 订单开平标志
    Open = '0', '开'
    Close = '1', '平'
    ForceClose = '2', '强平'
    CloseToday = '3', '平'
    CloseYesterday = '4', '平昨'
    ForceOff = '5', '强减'
    LocalForceClose = '6', '本地强平'


class OffsetFlag(models.TextChoices):  # 开平标志
    Open = '0', '开'
    Close = '1', '平'
    ForceClose = '2', '强平'
    CloseToday = '3', '平今'
    CloseYesterday = '4', '平昨'
    ForceOff = '5', '强减'
    LocalForceClose = '6', '本地强平'


class OrderStatus(models.TextChoices):  # 报单状态
    AllTraded = '0', '全部成交'
    PartTradedQueueing = '1', '部分成交还在队列中'
    PartTradedNotQueueing = '2', '部分成交不在队列中'
    NoTradeQueueing = '3', '未成交还在队列中'
    NoTradeNotQueueing = '4', '未成交不在队列中'
    Canceled = '5', '撤单'
    Unknown = 'a', '未知'
    NotTouched = 'b', '尚未触发'
    Touched = 'c', '已触发'


class OrderSubmitStatus(models.TextChoices):  # 报单提交状态
    InsertSubmitted = '0', '已经提交'
    CancelSubmitted = '1', '撤单已经提交'
    ModifySubmitted = '2', '修改已经提交'
    Accepted = '3', '已经接受'
    InsertRejected = '4', '报单已经被拒绝'
    CancelRejected = '5', '撤单已经被拒绝'
    ModifyRejected = '6', '改单已经被拒绝'


DCE_NAME_CODE = {
    '豆一': 'a',
    '豆二': 'b',
    '胶合板': 'bb',
    '玉米': 'c',
    '玉米淀粉': 'cs',
    '纤维板': 'fb',
    '铁矿石': 'i',
    '焦炭': 'j',
    '鸡蛋': 'jd',
    '焦煤': 'jm',
    '聚乙烯': 'l',
    '豆粕': 'm',
    '棕榈油': 'p',
    '聚丙烯': 'pp',
    '聚氯乙烯': 'v',
    '苯乙烯': 'eb',
    '乙二醇': 'eg',
    '液化石油气': 'pg',
    '生猪': 'lh',
    '粳米': 'rr',
    '豆油': 'y',
    '原木': 'lg',
    '纯苯': 'bz',
}

MONTH_CODE = {
    1: "F",
    2: "G",
    3: "H",
    4: "J",
    5: "K",
    6: "M",
    7: "N",
    8: "Q",
    9: "U",
    10: "V",
    11: "X",
    12: "Z"
}


KT_MARKET = {
    'DL': 'DCE',
    'DY': 'DCE',
    'SQ': 'SHFE',
    'SY': 'SHFE',
    'ZJ': 'CFFEX',
    'ZZ': 'CZCE',
    'ZY': 'CZCE',
}


class SignalType(models.TextChoices):
    ROLL_CLOSE = 'ROLL_CLOSE', '换月平旧'
    ROLL_OPEN = 'ROLL_OPEN', '换月开新'
    BUY = 'BUY', '买开'
    SELL_SHORT = 'SELL_SHORT', '卖开'
    SELL = 'SELL', '卖平'
    BUY_COVER = 'BUY_COVER', '买平'


class PriorityType(models.IntegerChoices):
    LOW = 0, '低'
    Normal = 1, '普通'
    High = 2, '高'
