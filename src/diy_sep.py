"""
author: hu yuxin
date: 2019/8/28

用于分隔中国收费系统中常见的地址栏信息的规则分词
Use to Separate the words of detailed address information, to get key words of different kinds of stores or companies

数据说明：
Data description:
一般存在的类别分为线上和线下消费记录
 records divided by channels : online or offline
 nowadays, in China, there are two main channel: Alipay and Tenpay which people always bind their credit cards on.
 线上记录在进行记录时会出现分隔符，”， , - — :"等，这些分隔符成为了线上记录的标志，同时往往最后一个分割信息是商户的具体信息
 significantly, the online records will usually contains seps, such as ", ，- —"etc. meanwhile， seps are specific for
 online records. Constantly, the last separation is the detailed information for shops or companies.
 排除线上和线下记录的不同点，一致要分割出的部分是商户信息中的类型信息、地理位置信息
 except for differences between online and offline, must get the management type and location information from address
 另外：由于报文对字符串的长度有限制，所以会出现不完整但有极强暗示完整信息的地址，设计进行补全
 by the way, the bank system has the limitation on the length of address, so that there will be some incomplete but with
 the remaining has strong implications, which we can design to complete.

使用资料：
reference materials:
中国所有省级行政区划地区名
all provinces in China
中国所有省会城市名
all provincial capital in China
对应的补完方式对应(自己设计)
the collection for incomplete —> complete（diy）
公司或店铺经营类型的后缀(自己收集)
the suffice of company and store to imply the management types（collected by myself）

"""
import pandas as pd


# 平台名 Common payment channels
payment_channels = pd.read_csv('../data/payment_channels.txt', header=None, encoding='gbk').values.tolist()
# 省级行政区划信息 province
province_list = pd.read_csv('../data/province.txt', header=None, encoding='gbk').values.tolist()
# 省会信息 center_city
center_city_list = pd.read_csv('../data/center_city.txt', header=None, encoding='gbk').values.tolist()
# 分割符号 seps
sep_list = pd.read_csv('../data/sep.txt', header=None, encoding='gbk', delimiter="\n").values.tolist()
# 后缀名 suffice
suffix_list = pd.read_csv('../data/company_type.txt', header=None, encoding='gbk').values.tolist()
# 补全对照表 part_full_table (type: DataFrame)
part_full_df = pd.read_csv('../data/part_company.txt', header=None, encoding='gbk')
# 经营类型表
company_list = pd.read_csv('../data/company_type.txt', header=None, encoding='gbk').values.tolist()


# # 字符过多，财付通分割
# def wechat_split(info, item):
#     wechat_list = ['财付通委托扣款方式', '财付通委托扣款方', '财付通委托扣款', '财付通委托扣', '财付通委托', '财付通委',
#                    '财付通', '财付']
#     for i, we in enumerate(wechat_list):
#         flag = 0
#         index = item.find(we, 0)
#         if index != -1:
#             flag = 1
#             info['线上标识'] = '1'
#             info['分割_1'] = '财付通委托扣款方式'
#             if index == 0:
#                 info['分割_2'] = item[index+(10-i):]
#                 item = item[index+(10-i):]
#                 return flag, info, item
#             else:
#                 info['分割_2'] = item[:index]
#                 item = item[:index]
#                 return flag, info, item
#     else:
#         return flag, info, item


# 特殊字符分割
def sep_middle(info, item):
    titles = ['sep_first', 'sep_last']
    for sep in sep_list:
        index_ = item.find(sep, 0)
        if index_ != -1:
            info['online_sign'] = '1'
            items = item.split(sep)
            info[titles[0]] = items[0]
            info[titles[1]] = items[-1]
            rest = items[-1]
            return 1, info, rest
    else:
        return 0, info, item


# 中划线出现常伴随字符串过长被截断情形
# 针对可推测的情况进行补全
def part_company(info, item):
    part_list = part_full_df[0].values.tolist()
    full_list = part_full_df[1].values.tolist()
    item_ends = [item[-5:], item[-4:], item[-3:], item[-2:]]
    for i, item_end in enumerate(item_ends):
        if item_end in part_list:
            index = part_list.index(item_end)
            info['management_type'] = full_list[index]
            item = item[:-(5-i)]+full_list[index]
            return info, item
    else:
        return info, item


# # 括号分割,将括号中的内容取出，并合并字符，考虑只有左括号的情形
def sep_brackets(info, item):
    index_right = item.find('）', 0)
    index_left = item.find('（', 0)
    if index_right != -1:
        info['bracket_content'] = item[index_left+1:index_right]
        item = item[0:index_left]+item[index_right+1:]
        return info, item
    elif index_left != -1:
        info['bracket_content'] = item[index_left+1:]
        item = item[0:index_left]
        return info, item
    else:
        return info, item


# # 将公司部分的信息切割
def company_split(info, item):
    for com in company_list:
        index = item.find(com[0], 0)
        if index != -1:
            info['management_type'] = com[0]
            item = item[:index]
            return info, item
    else:
        return info, item


# 地理位置的切割
def geography_split(info, item):
    for pro in province_list:
        index = item.find(pro[0], 0)
        pro_len = len(pro[0])
        if index != -1:
            info['province'] = pro[0]
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
    for pro in center_city_list:
        index = item.find(pro[0], 0)
        pro_len = len(pro[0])
        if index != -1:
            info['city'] = pro[0]
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
            info['city'] = item[:index+1]
            item = item[index+1:]
            return info, item
        else:
            return info, item
    else:
        return info, item


def main_split(file_path):
    names = pd.read_csv(file_path, dtype=str, encoding='gbk', header=None, engine='python').values.tolist()
    final_list = []
    for name in names:
        print(name)
        name_in_use = name[0]
        res0 = {'origin': name_in_use}
        flag1, res1, item1 = sep_middle(res0, name[0])
        # flag2, res2, item2 = wechat_split(res0, name[0])
        if flag1 == 1:
            res_new, rest = part_company(res1, item1)
            res_new1, rest1 = geography_split(res_new, rest)
            res_new2, rest2 = center_city_split(res_new1, rest1)
            res_final, rest_final = city_split(res_new2, rest2)
            res_final['name'] = rest_final
            final_list.append(res_final)
        # elif flag2 == 1:
        #     res_new, rest = part_company(res2, item2)
        #     res_new1, rest1 = geography_split(res_new, rest)
        #     res_new2, rest2 = center_city_split(res_new1, rest1)
        #     res_final, rest_final = city_split(res_new2, rest2)
        #     res_final['name'] = rest_final
        #     print(res_final)
        #     final_list.append(res_final)
        else:
            res1, name1 = sep_brackets(res0, name_in_use)
            res2, name2 = geography_split(res1, name1)
            res21, name21 = center_city_split(res2, name2)
            res3, name3 = company_split(res21, name21)
            res4, name4 = city_split(res3, name3)
            res4['name'] = name4
            print(res4)
            final_list.append(res4)
    df = pd.DataFrame(final_list)
    df = df[['origin', 'online_sign', 'province', 'city', 'name', 'management_type', 'bracket_content',
             'sep_first', 'sep_last']]
    df.to_csv('../data/result.csv',  index=None)


if __name__ == '__main__':
    file_path = ''
    main_split(file_path)

