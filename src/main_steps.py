from src import timestamp_to_date,mkdir
from src.main_generate_address import main_generate_address
from src.main_split import main_split
from src.main_cut_suffix import main_cut_suffix
from src.main_name_frequency import main_name_frequency


if __name__ == '__main__':
    time_suffix = timestamp_to_date()
    target_folder = '../generate_data/' + time_suffix + '/'
    mkdir(target_folder)
    print('时间戳为：', time_suffix, '生成的所有中间文件会存储于'+target_folder+'文件夹中')

    print('开始生成原始数据：')
    data = main_generate_address(ratio=0.5, total=100000, result_folder=target_folder, result_name='raw_names.txt')

    print('进行数据分割')
    sep_data = main_split(data, result_folder=target_folder, result_name='sep_result.csv')

    print('进行有效字段清洗')
    clean_data = main_cut_suffix(sep_data, col_name='name', result_folder=target_folder,
                                 result_name='cleaned_result.txt')

    print('进行字典汇总')
    dic_data = main_name_frequency(clean_data, result_folder=target_folder, result_name='dic_result.txt')
