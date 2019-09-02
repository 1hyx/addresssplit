# __*_ coding:utf-8 _*_
"""
在信息切割之后，需要整理出唯一性信息，做成字典
After the split of different type of information from every each of the address the rest still has useless words
切割掉的是后缀信息 有限公司/XXx公司系列的后缀的信息，以获得唯一的名称
cut several suffice to obtain unique names
"""
import pandas as pd


suffix_without_list = pd.read_csv('../data/suffix_without.txt', encoding='gbk', header=None).values.tolist()
suffix_within_list = pd.read_csv('../data/suffix_within.txt', header=None).values.tolist()


def cut_suffix_within(item):
    for suffix in suffix_within_list:
        index = item.find(suffix[0], 0)
        if index >= 0:
            more_len = len(suffix[0])
            item = item[:index+more_len]
            return 1, item
    return 0, item


def cut_suffix_without(item):
    for suf_2 in suffix_without_list:
        index = item.find(suf_2[0], 0)
        if index >= 0:
            item = item[:index]
            return 1, item
    return 0, item


def main_cut_suffix(file, col_name, result_folder, result_name):
    if type(file) == str:
        names = pd.read_csv(file, dtype=str)[col_name].values.tolist()
    else:
        names = file
    result_path = result_folder + result_name
    result = []
    n = len(names)
    for i, name in enumerate(names):
        flag1, rest1 = cut_suffix_within(str(name))
        flag2, rest2 = cut_suffix_without(str(name))
        if flag1:
            result.append(rest1)
        else:
            result.append(rest2)
        if i + 1 == n:
            percent = 100.0
            print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, n), end='\n')
        else:
            percent = round(1.0 * i / n * 100, 2)
            print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, n), end='\r')
    final_df = pd.DataFrame(result, columns=['rest_name']).to_csv(result_path, encoding='utf-8', index=None)
    return result_path
