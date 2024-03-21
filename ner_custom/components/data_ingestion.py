from email import header
import sys
from typing import Tuple
import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split
# from langdetect import detect
from ner_custom.entity.config_entity import DataIngestionConfig
from ner_custom.entity.artifact_entity import DataIngestionArtifact
from ner_custom.exception import MyException
from ner_custom.logger import logging
from ner_custom.utils.main_utils import *
from ner_custom.data_access.data import Data
from typing import List
import os

from ner_custom.logger import logging
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        :param data_ingestion_config: configuration for data ingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e,sys)

    def export_data_into_feature_store(self)->DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from SQL Server to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info(f"Exporting data from SQL Client")
            data = Data()
            dataframe = data.export_collection_as_dataframe()
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path  = self.data_ingestion_config.feature_store_file_path
            print(f"This is feature store file path {feature_store_file_path}")
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False, header=True, escapechar="\\")
            print("I am here")
            return dataframe

        except Exception as e:
            raise MyException(e,sys)
        
    def add_space_to_amount(self, dataframe: DataFrame) -> DataFrame:
        '''
        Giving space in between any amount values before and after`
        '''
        try: 
            raw_columns = self._schema_config['message_columns'][0]
            # print(f"This is raw columns: {raw_columns}")
            # print(f"this is data frame in the function: {dataframe[raw_columns]}")
            for i in range(len(dataframe[raw_columns])):
                # print("******\n",dataframe[raw_columns][i])
                if type(dataframe[raw_columns][i])==str:
                    modified_sentence = re.sub(r"(₹|Rs\.)", r"\1 ", dataframe[raw_columns][i])
                    modified_sentence = modified_sentence.replace("'"," ")
                    dataframe[raw_columns][i] = modified_sentence

            return dataframe  
        except Exception as e:
            raise MyException(e,sys)  
        
    def add_space_after_amount(self, dataframe: DataFrame) -> DataFrame:
        '''
        Giving space in between any amount values before and after
        '''
        try: 
            raw_columns = self._schema_config['message_columns'][0]
            
            for i in range(len(dataframe[raw_columns])):
                # print("******\n",dataframe[raw_columns][i])
                if type(dataframe[raw_columns][i])==str:
                    pattern = r'(\d+)/-'
                    modified_sentence = re.sub(pattern, r'\1 /-', dataframe[raw_columns][i])
                    dataframe[raw_columns][i] = modified_sentence
            return dataframe  
        except Exception as e:
            raise MyException(e,sys)  
        
    def add_space_before_bank(self, dataframe: DataFrame) -> DataFrame:
        '''
        Giving space in between any amount values before and after
        '''
        try: 
            raw_columns = self._schema_config['message_columns'][0]
            word_list = ['BOB','Canara','HDFC']
            for i in range(len(dataframe[raw_columns])):
                for word in word_list:
                # print("******\n",dataframe[raw_columns][i])
                    if type(dataframe[raw_columns][i])==str:
                        pattern = r'-(\b' + re.escape(word) + r'\b)'
                        modified_sentence = re.sub(pattern, r' - \1', dataframe[raw_columns][i])
                        dataframe[raw_columns][i] = modified_sentence

            return dataframe  
        except Exception as e:
            raise MyException(e,sys)  

    def add_space1(self, dataframe: DataFrame) -> DataFrame:
        '''
        Giving space in between any amount values before and after
        '''
        try: 
            raw_columns = self._schema_config['message_columns'][0]
            word_list = ['BOB','Canara','HDFC']
            for i in range(len(dataframe[raw_columns])):
            
            # print("******\n",dataframe[raw_columns][i])
                if type(dataframe[raw_columns][i])==str:
                    pattern = r'Rs(\d+)'
                    modified_sentence = re.sub(pattern, r'Rs \1', dataframe[raw_columns][i])
                    modified_sentence = modified_sentence.replace('-',' ')
                    dataframe[raw_columns][i] = modified_sentence

            return dataframe  
        except Exception as e:
            raise MyException(e,sys)
        
    def add_start_space(self, dataframe: DataFrame) -> DataFrame:
        '''
        Giving space in between any amount values before and after
        '''
        try: 
            raw_columns = self._schema_config['message_columns'][0]
            for i in range(len(dataframe[raw_columns])):
            
            # print("******\n",dataframe[raw_columns][i])
                if type(dataframe[raw_columns][i])==str:
                    modified_sentence = re.sub(r"'", '"', dataframe[raw_columns][i])
                    dataframe[raw_columns][i] = modified_sentence

            return dataframe  
        except Exception as e:
            raise MyException(e,sys)
        

        

    def split_data_as_train_test(self,dataframe: DataFrame) ->None:
        """
        Method Name :   split_data_as_train_test
        Description :   This method splits the dataframe into train set and test set based on split ratio 
        
        Output      :   Folder is created in s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")

        try:
 
            train_set, val_set, test_set = np.split(dataframe.sample(frac=1, random_state=42),
                            [int(.8 * len(dataframe)), int(.9 * len(dataframe))])

            logging.info("Performed train test split on the dataframe")
            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            raw_columns = self._schema_config['message_columns']
            print("raw Columns is ",raw_columns)
            #Saving the dataframe specific column in a path
            # print("File Path is ",self.data_ingestion_config.feature_store_file_path)

            dataframe_to_text_file(dataframe, raw_columns, self.data_ingestion_config.text_file_path)

            logging.info(f"Exporting train and test file path.")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            val_set.to_csv(self.data_ingestion_config.validation_file_path,index=False,header=True)

            logging.info(f"Exported train and test and validation file path.")
        except Exception as e:
            raise MyException(e, sys) from e

    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   train set and test set are returned as the artifacts of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")

        try:
            dataframe = self.export_data_into_feature_store()

            logging.info("Got the data from mongodb")

            # self.add_start_space(dataframe)
            self.add_space_to_amount(dataframe)
            self.add_space_after_amount(dataframe)
            self.add_space_before_bank(dataframe)
            self.add_space1(dataframe)
            
            # self.add_space_before_bank(dataframe)

            # self.add_space_to_policy_number(dataframe)

            logging.info("Added spaces before the entities as needed")

            self.split_data_as_train_test(dataframe)

            logging.info("Performed train test split on the dataset")

            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e, sys) from e
        
# if __name__=="__main__":
#     obj = DataIngestion()
#     df=obj.export_data_into_feature_store()
#     # print(df['SMS_Details'])
#     df_new = obj.add_space_to_amount(df)
#     # print(df_new['SMS_Details'])