import time
import os





def timestamp_to_date(format_string="%Y_%m_%d_%H_%M_%S"):
    time_array = time.localtime()
    str_date = time.strftime(format_string, time_array)
    return str_date


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    return path
