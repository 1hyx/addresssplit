# 测试处理器核数 由于数据分割任务可以分割，建议使用多进程
# to test the num of kernels of your cpu. as the work can be divided completely, advise using multi-process

import multiprocessing as mp

if __name__ == '__main__':
    process_num = mp.cpu_count()
    print(process_num)
