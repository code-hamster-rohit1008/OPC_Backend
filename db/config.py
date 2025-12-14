from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os

uri = "mongodb+srv://"+ quote_plus(os.getenv("DB_USER")) + ":" + quote_plus(os.getenv("DB_PASSWORD")) + "@opc.fimitv0.mongodb.net/?appName=OPC"

client = MongoClient(uri, server_api=ServerApi('1'))