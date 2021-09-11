import pymongo 
import json
from pymongo import MongoClient 

# Making Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db=client["openvasdb"]

     
# Created or Switched to collection 
# names: GeeksForGeeks
Collection = db["vul_reports"]
  
# Loading or Opening the json file
with open('report.json') as file:
    file_data = json.load(file)
      
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    Collection.insert_many(file_data)  
else:
    Collection.insert_one(file_data)