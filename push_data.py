import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

import pandas as pd
from pymongo import MongoClient

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logger


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def csv_to_json(self, file_path):
        """
        Converts a CSV file into a list of JSON records.
        """
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            records = list(json.loads(data.T.to_json()).values())

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def insert_data_mongodb(self, records, database, collection):
        """
        Inserts records into MongoDB.
        """
        try:
            self.mongo_client = MongoClient(
                MONGO_DB_URL,
                tlsCAFile=ca
            )

            self.database = self.mongo_client[database]
            self.collection = self.database[collection]

            self.collection.insert_many(records)

            logger.info(f"{len(records)} records inserted into MongoDB.")

            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "NetworkSecurity"
    COLLECTION = "NetworkData"

    network_obj = NetworkDataExtract()

    records = network_obj.csv_to_json(FILE_PATH)

    no_of_records = network_obj.insert_data_mongodb(
        records,
        DATABASE,
        COLLECTION
    )

    print(f"{no_of_records} records inserted successfully.")