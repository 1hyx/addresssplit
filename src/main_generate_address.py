"""
author: hu yuxin
date: 2019/8/30

用于生成不规则的交易地址
to generate different kinds of address
不规则地址的模式抽样, 有几种模式
irregular address, conclude into several mods
an address can be constructed by payment_channel, suffix, location with length less than 20
1. 支付宝，支付宝外部商户，XX商户(,可能被替换为- ,),分隔符在sep.txt，交易平台信息在payment_channels.txt
2. (地点)某省某市XX有限公司（有限公司可被替换为 公司 有限责任公司 信息公司 信息技术公司等，后缀在suffix.txt
3. 地点信息省级行政区划在 province.txt (包含 xxx省和xxx 两种情况)
4. 省会城市信息在center_city.txt（包含 xx市和xx 两种情况）
5. 可能出现其他市的情况，随机组合字+"市"生成
6. 设定字符串的长度为19，在完成生成之后最后进行截断，模拟报文过长被数据库截断的情形

ps. 线上报文的格式规则  online trade has specific mod of address
    if online , use 1.2.3.4.5.6
    else use 2.3.4.5.6
"""

import random
from random import choice
import pandas as pd


# 常见公司名 28W Common company name with size 280,000
# the file downloaded from https://codeload.github.com/fighting41love/funNLP/zip/master 中的 公司名大全
all_company_list = pd.read_csv('../data/Company_dictionary.txt', header=None, encoding='utf-8').sample(500).\
    values.tolist()
# 平台名 Common payment channels
payment_channels = pd.read_csv('../data/payment_channels.txt', header=None, encoding='gbk').values.tolist()
# 省级行政区划信息 province
province_list = pd.read_csv('../data/province.txt', header=None, encoding='gbk').values.tolist()
# 省会信息 center_city
center_city_list = pd.read_csv('../data/center_city.txt', header=None, encoding='gbk').values.tolist()
# 分割符号 seps
sep_list = pd.read_csv('../data/sep.txt', header=None, encoding='gbk', delimiter="\n").values.tolist()
# 后缀名
suffix_list = pd.read_csv('../data/company_type.txt', header=None, encoding='gbk').values.tolist()


# 利用信息生成线上报文的数据
# Use materials to generate the information that match the rules of online consumption
def generate_online_address(n):
    item_list = []
    print('开始生成{}条线上数据'.format(n))
    for i in range(n):
        # design two types with a few differences
        if i % 3 == 0:
            item = choice(payment_channels)[0]+choice(sep_list)[0]+choice(province_list)[0]+choice(all_company_list)[0]\
                   + choice(suffix_list)[0] + "XX分公司"
        else:
            item = choice(payment_channels)[0]+choice(sep_list)[0]+'('+choice(province_list)[0]+')'\
                   + choice(all_company_list)[0] + choice(suffix_list)[0]
        item_list.append(item)
        if i + 1 == n:
            percent = 100.0
            print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, n), end='\n')
        elif i % 100 == 0:
            percent = round(1.0 * i / n * 100, 2)
            print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, n), end='\r')
    return item_list


# 利用信息生成线下报文的数据
# Use materials to generate the information that match the rules of offline consumption
def generate_offline_address(n):
    item_list = []
    print('开始生成{}条线下数据'.format(n))
    for i in range(n):
        if i % 2 == 0:
            item = choice(province_list)[0] + choice(all_company_list)[0] + choice(suffix_list)[0]
        elif i % 3 == 0:
            item = choice(all_company_list)[0] + '(' + choice(province_list)[0] + ')' + choice(suffix_list)[0]
        elif i % 5 == 0:
            item = choice(all_company_list)[0] + '(' + choice(center_city_list)[0] + ')' + choice(suffix_list)[0]
        else:
            item = 'XX市' + choice(all_company_list)[0] + choice(suffix_list)[0]
        item_list.append(item)
        if i + 1 == n:
            percent = 100.0
            print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, n), end='\n')
        else:
            percent = round(1.0 * i / n * 100, 2)
            print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, n), end='\r')
    return item_list


# 用于控制生成数据的量和线上线下比例
# use to control the amount of address and the ratio of online: offline
# ratio := the amount of online: total
# total := the amount of address for the function to generate
def main_generate_address(ratio, total, result_folder, result_name, stop=20):
    result_path = result_folder + result_name
    n1 = int(total*ratio)
    n2 = total-n1
    print('will generate {} online address and {} offline address'.format(n1, n2))
    item_list1 = generate_online_address(n1)
    item_list2 = generate_offline_address(n2)
    items = item_list1+item_list2
    random.shuffle(items)
    df = pd.DataFrame(items, columns=['names'])['names'].str.slice(stop=stop)
    df.to_csv(result_path, encoding='utf-8', index=None)
    print('{} address have been generated at {} '.format(total, result_path))
    return result_path
