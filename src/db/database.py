import pymongo


class Database(object):
    # URI = "mongodb://127.0.0.1:27017"
    URI = "mongodb://ishween:isha%401999@cluster0-shard-00-00-firjr.mongodb.net:27017,cluster0-shard-00-01-firjr.mongodb.net:27017,cluster0-shard-00-02-firjr.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['Reimburse']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def delete(collection, query):
        Database.DATABASE[collection].remove(query)
