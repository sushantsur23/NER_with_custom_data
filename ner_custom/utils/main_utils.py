import os.path
# import shutil
import sys, os, re
from typing import Dict
import numpy as np
import dill, json
# import xgboost
import yaml
from pandas import DataFrame

import pandas as pd
# from sklearn.metrics import roc_auc_score
# from sklearn.model_selection import GridSearchCV
# from sklearn.utils import all_estimators
# from yaml import safe_dump

from ner_custom.constant import MODEL_TRAINER_MODEL_CONFIG_FILE_PATH, SCHEMA_FILE_PATH
from ner_custom.exception import MyException
from ner_custom.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise MyException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise MyException(e, sys)


def load_object(file_path: str) -> object:
    logging.info("Entered the load_object method of utils")

    try:
        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info("Exited the load_object method of utils")

        return obj

    except Exception as e:
        raise MyException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise MyException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MyException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of utils")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of utils")

    except Exception as e:
        raise MyException(e, sys) from e


def drop_columns(df: DataFrame, cols: list)-> DataFrame:

    """
    drop the columns form a pandas DataFrame
    df: pandas DataFrame
    cols: list of columns to be dropped
    """
    logging.info("Entered drop_columns methon of utils")

    try:
        df = df.drop(columns=cols, axis=1)

        logging.info("Exited the drop_columns method of utils")
        
        return df
    except Exception as e:
        raise MyException(e, sys) from e

def get_file_path():
    '''
    Function created to ask for a specific file path
    '''
    try:
        file_path = input("Enter the path of the annotation file: ")
        if os.path.isfile(file_path):
            return file_path
    except Exception as e:
        logging.info("Invalid file path. Please try again.")
        raise MyException(e, sys) from e



def convert_column_to_txt(df, column_name, txt_file, file_path=''):
    '''
    Function created to convert one column of dataframe and convert it to text file and output the same.
    '''
    try:
        logging.info("Starting to create the text file for the required column")
        selected_column = df[column_name]
        output_path = os.path.join(file_path, txt_file) if file_path else txt_file
        selected_column.to_csv(output_path, index=False, header=False)

        # Example usage:
        # df = pd.read_csv('data.csv')  # Replace 'data.csv' with your actual DataFrame file

        column_name = 'new_column_name'  # Replace 'column_name' with the name of the column you want to convert
        txt_file = 'annotations.txt'  # Replace 'output.txt' with the desired name of the output .txt file
        logging.info("Creation of txt file ready for creating the annotation.")

        # file_path = './additional_folder'  # Replace './additional_folder' with the desired additional path
    except Exception as e:
        raise MyException(e, sys) from e


def read_json_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

#Function to convert csv to text file for annotations
def dataframe_to_text_file(dataframe, column_name, file_path):
    column_data = dataframe[column_name].values[1:]
    file_path = file_path + ".txt"
    
    with open(file_path, 'w+', encoding='utf-8') as file:
        for value in column_data:
            file.write(str(value) + '\n')
    
    print(f"The column '{column_name}' has been successfully written to '{file_path}' as a text file.")

#Function to add space after keyword Rs.
def add_space_after_keyword(sentence):
    keyword = "Rs."
    keyword_index = sentence.find(keyword)
    if isinstance(sentence, str):
        pattern = r"\b(\d+(?:\.\d{1,2})?)\b"
        modified_sentence = re.sub(pattern, r' \1', sentence)       
        return modified_sentence
    else :
        return sentence

# def add_space1(sentence):
#     pattern1 = r"(Rs\.)"
#     pattern2 = r"(?<!\d)\d+(?:\.\d{1,2})?(?!\d)"
#     if isinstance(sentence, str):
#         if re.search(pattern1, sentence):
#             modified_sentence = re.sub(pattern1, r"\1 ", sentence)
#             return modified_sentence
#         # elif re.search(pattern2, sentence):
#         #     modified_sentence = re.sub(pattern2, r" \1", sentence)
#         #     return modified_sentence
#         else:
#             return sentence

#Add spaces before bank names    
def add_space_before_bank(text_series):
    keywords = ['Canara Bank', 'Kotak Mahindra Bank', 'Indian Bank', 'Axis Bank']
    modified_text_series = text_series.copy()
    for i, text in enumerate(modified_text_series):
        for keyword in keywords:
            lowercase_keyword = keyword.lower()
            if text.lower().find(lowercase_keyword) != -1 and not text.lower().startswith(lowercase_keyword):
                modified_text_series[i] = text.replace(lowercase_keyword, ' ' + lowercase_keyword)
            uppercase_keyword = keyword.upper()
            if text.upper().find(uppercase_keyword) != -1 and not text.upper().startswith(uppercase_keyword):
                modified_text_series[i] = text.replace(uppercase_keyword, ' ' + uppercase_keyword)
            titlecase_keyword = keyword.title()
            if text.title().find(titlecase_keyword) != -1 and not text.title().startswith(titlecase_keyword):
                modified_text_series[i] = text.replace(titlecase_keyword, ' ' + titlecase_keyword)
    return modified_text_series