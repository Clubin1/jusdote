from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://justin03tubay:j4podRLoAb7pZVJt@cluster0.zfgelwf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['db']