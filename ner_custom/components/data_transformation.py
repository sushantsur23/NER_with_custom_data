import sys, os
import numpy as np
import pandas as pd
from ner_custom.constant import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from ner_custom.entity.config_entity import DataTransformationConfig
from ner_custom.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from ner_custom.exception import MyException
from ner_custom.logger import logging
from ner_custom.utils.main_utils import *
from langdetect import detect
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer
from sklearn.compose import ColumnTransformer


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            # self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e, sys)

    def transformed_dataframe(self,train_df) -> DataFrame:
         #here we combine the data received from the anotations file to existing dataframe
        #train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
        try:     
            json_file_path = input("Enter the file path of the JSON file: ")
            json_df = pd.read_json(json_file_path)

            train_df = pd.concat([train_df, json_df], axis=1)
            return train_df
        except Exception as e:
            raise MyException(e, sys)
             
    def extract_labels(self,train_df) -> DataFrame:
        #This function will extract the labels properly in the dataframe 
        try:
            st_list =[]
            text_list=[]
            for i in range(len(train_df)):
                

            pass
        except Exception as e:
            raise MyException(e, sys)


       
    def get_data_transformer_object(self) -> Pipeline:
            """
            Method Name :   get_data_transformer_object
            Description :   This method creates and returns a data transformer object for the data
            
            Output      :   data transformer object is created and returned 
            On Failure  :   Write an exception log and then raise an exception
            """
            logging.info(
                "Entered get_data_transformer_object method of DataTransformation class"
            )

            try:
                logging.info("Make necessary changes to the Raw SMS data")


                logging.info("Initialized Functions to add space wherever needed")
                raw_columns = self._schema_config['message_columns']

                logging.info("Initialize PowerTransformer")

                transform_pipe = Pipeline(steps=[
                    ('transformer', PowerTransformer(method='yeo-johnson'))
                ])
                
                preprocessor = ColumnTransformer(
                [
                    ("SpaceToAmount", space_to_amt, raw_columns),
                    ("SpaceToDate", space_to_date, raw_columns),
                    ("SpaceToPolicy", space_to_policy, raw_columns),

                ]
            )
                logging.info("Created preprocessor object from ColumnTransformer")
                
                logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )
                return preprocessor

            except Exception as e:
                raise MyException(e, sys) from e
            
    def initiate_data_transformation(self,dataframe: DataFrame) -> DataTransformationArtifact:
            """
            Method Name :   initiate_data_transformation
            Description :   This method initiates the data transformation component for the pipeline 
            
            Output      :   data transformer steps are performed and preprocessor object is created  
            On Failure  :   Write an exception log and then raise an exception
            """
            try:
                if detect(dataframe['SMS_Details'])=='en':
                    dataframe['SMS_Details'] = dataframe['SMS_Details'].apply(add_space_to_amount)
                    dataframe['SMS_Details'] = dataframe['SMS_Details'].apply(add_space_to_date)
                    dataframe['SMS_Details'] = dataframe['SMS_Details'].apply(add_spaces_to_policy_number)

                    dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
                    os.makedirs(dir_path,exist_ok=True)
                    logging.info(f"Exporting text file for the dataframe in training file path.")    

                    # train_set['SMS_Details'].to_txt

                    #Call all the required functions and return all Data Transformation Artifact
                    pass
                    
                    data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                    )  

                    logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
                    return data_transformation_artifact

            except Exception as e:
                raise MyException(e, sys) from e