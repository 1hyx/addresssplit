# 用于将生成的唯一标识统计不同名称出现的次数，同时生成对应字典

import pandas as pd


def main_name_frequency(file, result_folder, result_name):
    if type(file) == str:
        data = pd.read_csv(file)
    else:
        data = file
    result_path = result_folder + result_name

    res = data['rest_name'].value_counts()
    dictionary = pd.DataFrame(columns=['name', 'frequency'])
    dictionary['name'] = res.index.tolist()
    dictionary['frequency'] = res.values.tolist()
    dictionary.to_csv(result_path, index=None, encoding='utf-8')
    print('汇总完成！')
    return dictionary


