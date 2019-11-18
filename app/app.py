import pymongo

mongo_client = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/?authSource=admin&authMechanism=SCRAM-SHA-1&retryWrites=false".format('mongo-admin', 'password'))

app_db = mongo_client["app_db"]

review_col = app_db["review"]

for i in range(10000):
    mydict = { "name": "John", "address": "Highway 00{}".format(i) }
    status = review_col.insert_one(mydict)
print(status)