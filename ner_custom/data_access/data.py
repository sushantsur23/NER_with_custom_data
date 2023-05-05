import sys, os
from typing import Optional
import pymongo
import numpy as np
import pandas as pd
import json 
import certifi
from ner_custom.configuration.configuration_component import MongoDBClient
from ner_custom.constant.database import DATABASE_NAME
from ner_custom.exception import MyException
from ner_custom.constant.env_variable import MONGODB_URL_KEY
ca = certifi.where()


class MongoData:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:

            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                print("****",mongo_db_url)
                if "localhost" in mongo_db_url:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url) 
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e