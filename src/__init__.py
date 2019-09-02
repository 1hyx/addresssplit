import time
import os


# 汇总时间戳方法
def timestamp_to_date(format_string="%Y_%m_%d_%H_%M_%S"):
    time_array = time.localtime()
    str_date = time.strftime(format_string, time_array)
    return str_date


# 创建文件夹
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    return path
