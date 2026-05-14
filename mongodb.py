from pymongo import MongoClient

# Підключення до локального сервера MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Створюємо базу даних
db = client["dictionary_mongodb"]

# Створюємо колекції
words_collection = db["words"]
languages_collection = db["languages"]

def get_mongo_db():
    return words_collection