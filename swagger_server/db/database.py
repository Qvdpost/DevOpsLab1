from pymongo import MongoClient
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=Singleton):
    def __init__(self):
        self.client = MongoClient(f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@" +
                                  f"{os.environ['MONGODB_HOSTNAME']}:{os.environ['MONGODB_PORT']}/")

        self.db = self.client[os.environ['MONGODB_DATABASE']]


class Collection:
    def __init__(self, db, collection):
        self.db = db.db
        self.collection = self.db[collection]

    def create(self, item):
        doc = self.collection.insert_one(item)
        return doc.inserted_id

    def retrieve(self, uid):
        return self.collection.find_one({"_id": uid})

    def update(self, mode, uid, item):
        if mode == "push":
            return self.collection.update_one({"_id": uid}, {'$push': item})
        elif mode == "set":
            return self.collection.update_one({"_id": uid}, {'set': item})

        raise NotImplementedError()

    def delete(self, uid):
        return self.collection.delete_one({"_id": uid})
