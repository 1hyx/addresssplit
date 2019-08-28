# 自定义分隔位置分词法
import pandas as pd
import re


# 字符过多，财付通分割
def wechat_split(info, item):
    wechat_list = ['财付通委托扣款方式', '财付通委托扣款方', '财付通委托扣款', '财付通委托扣', '财付通委托', '财付通委',
                   '财付通', '财付']
    for i, we in enumerate(wechat_list):
        flag = 0
        index = item.find(we, 0)
        if index != -1:
            flag = 1
            info['线上标识'] = '1'
            info['分割_1'] = '财付通委托扣款方式'
            if index == 0:
                info['分割_2'] = item[index+(9-i):]
                item = item[index+(9-i):]
                return flag, info, item
            else:
                info['分割_2'] = item[:index]
                item = item[:index]
                return flag, info, item
    else:
        return flag, info, item


# 特殊字符分割
# # 中划线分割
def sep_middle(info, item):
    index_ = item.find('-', 0)
    index_dot = item.find('，', 0)
    Flag = 0
    titles = ['分割_1', '分割_2', '分割_3']
    if index_ != -1:
        info['线上标识'] = '1'
        items = re.split('-', item)
        for i, it in enumerate(items):
            info[titles[i]] = it
        Flag = 1
        rest = items[-1]
        return Flag, info, rest
    elif index_dot != -1:
        info['线上标识'] = '1'
        items = re.split('，', item)
        for i, it in enumerate(items):
            info[titles[i]] = it
        Flag = 1
        rest = items[-1]
        return Flag, info, rest
    else:
        return Flag, info, item


# 中划线出现常伴随字符串过长被截断情形，对应公司信息中也有地理位置和公司类型信息要进行切割
def part_company(info, item):
    part_full_list = pd.read_csv('C://Users//EMIT003//Desktop//不完整公司后缀信息对应.txt', dtype=str, encoding='gbk',
                                 header=None, engine='python')
    part_list = part_full_list[0].values.tolist()
    full_list = part_full_list[1].values.tolist()
    item_ends = [item[-4:], item[-3:], item[-2:]]
    for i, item_end in enumerate(item_ends):
        if item_end in part_list:
            index = part_list.index(item_end)
            info['商户类型'] = full_list[index]
            item = item[:-(4-i)]+full_list[index]
            return info, item
    else:
        return info, item


# # 括号分割,将括号中的内容取出，并合并字符，考虑只有左括号的情形
def sep_brackets(info, item):
    index_right = item.find('）', 0)
    index_left = item.find('（', 0)
    if index_right != -1:
        info['括号内容'] = item[index_left+1:index_right]
        item = item[0:index_left]+item[index_right+1:]
        return info, item
    elif index_left != -1:
        info['括号内容'] = item[index_left+1:]
        item = item[0:index_left]
        return info, item
    else:
        return info, item


# # 将公司部分的信息切割
def company_split(info, item):
    company_list = pd.read_csv('C://Users//EMIT003//Desktop//公司类型.txt', dtype=str, encoding='gbk', header=None,
                               engine='python').values.tolist()
    for com in company_list:
        index = item.find(com[0], 0)
        com_len = len(com[0])
        if index != -1:
            info['商户类型'] = com[0]
            return info, item
    else:
        return info, item


# 地理位置的切割
def geography_split(info, item):
    province_list = pd.read_csv('C://Users//EMIT003//Desktop//省级行政区划.txt', dtype=str, encoding='gbk', header=None,
                                engine='python').values.tolist()
    for pro in province_list:
        index = item.find(pro[0], 0)
        pro_len = len(pro[0])
        if index != -1:
            info['省级行政区划'] = pro[0]
            if index == 0:
                item = item[index+pro_len:]
            else:
                item_temp = item[:index]+item[index+pro_len:]
                if item_temp.find('公司'):
                    item = item_temp
                else:
                    item = item[:index]
            return info, item
    else:
        return info, item


# 省会城市标签
def center_city_split(info, item):
    center_list = pd.read_csv('C://Users//EMIT003//Desktop//省会.txt', dtype=str, encoding='gbk', header=None,
                              engine='python').values.tolist()
    for pro in center_list:
        index = item.find(pro[0], 0)
        pro_len = len(pro[0])
        if index != -1:
            info['城市'] = pro[0]
            if index == 0:
                item = item[index + pro_len:]
            else:
                item = item[:index]
            return info, item
    else:
        return info, item


# 非省会非省地理信息切割
# 排除市本身的词汇情况：市区
def city_split(info, item):
    special = ['市区', '市民', '超市']
    f = 0
    for spe in special:
        pre_index = item.find(spe)
        if pre_index != -1:
            f = 1
            break
    if f == 0:
        index = item.find('市')
        if index != -1:
            info['城市'] = item[:index+1]
            item = item[index+1:]
            return info, item
        else:
            return info, item
    else:
        return info, item


def main_split(file_path):
    # names = pd.read_csv('C://Users//EMIT003//Desktop//示例商户名称.txt', dtype=str, encoding='gbk', header=None,
    #                     engine='python').values.tolist()
    names = pd.read_csv(file_path, dtype=str, encoding='gbk', header=None, engine='python').values.tolist()
    final_list = []
    for name in names:
        print(name)
        name_in_use = name[0]
        res0 = {'原始信息': name_in_use}
        flag1, res1, item1 = sep_middle(res0, name[0])
        flag2, res2, item2 = wechat_split(res0, name[0])
        if flag1 == 1:
            res_new, rest = part_company(res1, item1)
            res_new1, rest1 = geography_split(res_new, rest)
            res_new2, rest2 = center_city_split(res_new1, rest1)
            res_final, rest_final = city_split(res_new2, rest2)
            res_final['商户名称'] = rest_final
            final_list.append(res_final)
        elif flag2 == 1:
            res_new, rest = part_company(res2, item2)
            res_new1, rest1 = geography_split(res_new, rest)
            res_new2, rest2 = center_city_split(res_new1, rest1)
            res_final, rest_final = city_split(res_new2, rest2)
            res_final['商户名称'] = rest_final
            print(res_final)
            final_list.append(res_final)
        else:
            res1, name1 = sep_brackets(res0, name_in_use)
            res2, name2 = geography_split(res1, name1)
            res21, name21 = center_city_split(res2, name2)
            res3, name3 = company_split(res21, name21)
            res4, name4 = city_split(res3, name3)
            res4['商户名称'] = name4
            print(res4)
            final_list.append(res4)
    df = pd.DataFrame(final_list)
    df = df[['原始信息', '线上标识', '省级行政区划', '城市', '商户名称', '商户类型', '括号内容', '分割_1', '分割_2', '分割_3']]
    df.to_csv('C://Users//EMIT003//Desktop//分割结果.csv', index=None)


if __name__ == '__main__':
    file_path = ''
    main_split(file_path)

