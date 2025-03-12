import os
import sys
import json

from dotenv import load_dotenv


load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
# print(MONGO_DB_URL)

# a python packages that provides a set of root certificates
# used by python libraries that need to make secure http connections
# we are going to make http request to mongo db database, using request library,etc
# they trust only this certificate which is verified by trusted certified authorities
import certifi

# retireves the path to the bundle of ca (certificate authorities) certificates provided by certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def cv_to_json_convertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            # records will be a list of joson
            # we transpose it first, then convert it to json
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

# ETL Pipeline
if __name__ == '__main__':
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "Zeinab"
    Collection = "NetworkData"
    network_obj = NetworkDataExtract()
    records = network_obj.cv_to_json_convertor(file_path=FILE_PATH)
    no_of_records = network_obj.insert_data_mongodb(records,DATABASE,Collection)
    # at this point the data should be visible on mongo db -> clusters -> collections -> ...
    print(no_of_records)
