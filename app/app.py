import pymongo
import csv
import os


class Review(object):
    def __init__(self):
        self.mongo_client = pymongo.MongoClient("mongodb://{}:{}@localhost:27017/?authSource=admin&authMechanism=SCRAM-SHA-1&retryWrites=false".format('mongo-admin', 'password'))
        self.app_db = self.mongo_client["app_db"]
        self.collection = self.app_db["review"]

    def insert(self, review_dict):
        return self.collection.insert_one(review_dict)
    
    def insert_many(self, reviews):
        return self.collection.insert_many(reviews)

    def get_all(self):
        temp = []
        for row in self.collection.find():
            temp.append(row)
        return temp
    
    def get_where(self, where):
        temp = []
        for row in self.collection.find(where):
            temp.append(row)
        return temp

    def count_reviews_by_asin(self):
        temp = []
        for row in self.collection.aggregate([{ "$group": { "_id": "$asin", "total_reviews": { "$sum": 1 } } }]):
            temp.append(row)
        return temp

    def count_helpfulvotes_by_asin(self):
        temp = []
        for row in self.collection.aggregate([{ "$group": { "_id": "$asin", "total_helpfulvotes": { "$sum": "$helpfulVotes" } } }]):
            temp.append(row)
        return temp

    def update(self, where, new_values):
        updated = self.collection.update_many(where, { '$set' : new_values})
        print(updated.modified_count, "rows updated.")

    def delete(self, where):
        deleted = self.collection.delete_many(where)
        print(deleted.deleted_count, "rows deleted.")

review = Review()

# Importing Dataset

# with open(os.path.dirname(os.path.abspath(__file__))+'\\reviews.csv', encoding='utf-8', newline='\n') as file_csv:
#     reviews = csv.reader(file_csv, delimiter=',', )
#     reviews_arr = []
#     reviews_attribs = []
#     idx = 0
#     for row in reviews:
#         if idx == 0:
#             reviews_attribs = row
#         else:
#             if len(row) < len(reviews_attribs):
#                 continue
#             tmp = {}
#             try:
#                 for idx_attrib, attrib in enumerate(reviews_attribs):
#                     try:
#                         tmp[attrib] = float(row[idx_attrib])
#                     except:
#                         try:
#                             tmp[attrib] = row[idx_attrib]
#                         except:
#                             pass
#                 reviews_arr.append(tmp)
#             except:
#                 pass
#         idx += 1    
#     review.insert_many(reviews_arr)




#print(review.get_all()[90000])


#review.update({"name": "Token"}, {'rating':3.5})
#review.delete({"name": "Token"})


#print(review.count_helpfulvotes_by_asin())
#print(review.count_reviews_by_asin())
