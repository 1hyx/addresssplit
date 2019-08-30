# _*_ coding:utf-8 _*_
import pandas as pd

suffix = ['超市','酒店','宾馆','管理有限责任公司','管理有限公司','有限责任公司','有限公司','信息技术公司','信息科技公司','科技公司',]

def delete_suffix(data):
    for item in suffix:
        index = data.find(item, 0)
        if index != -1:
            data = data[:index]
        return data

if __name__ == '__main__':
