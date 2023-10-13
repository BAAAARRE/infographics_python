import glob
import pandas as pd


def load_data():
    """
    Load all csv file in a pandas dataframe from data folder, and put it in dict with file name as key and dataframe as value
    :return: dict.
    """
    list_data_all_path = glob.glob("data/*.csv")
    data_raw_dict = {}

    for data_all_path in list_data_all_path:
        file_name = data_all_path.split('\\')[-1]
        file_name_without_extension = file_name.split('.')[0]
        file_name_without_directory = file_name_without_extension.split('/')[-1]
        df = pd.read_csv(data_all_path)
        data_raw_dict[f'df_{file_name_without_directory}'] = df
    return data_raw_dict
