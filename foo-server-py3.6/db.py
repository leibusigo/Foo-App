import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)

db = client['foo-app']

coordinates = db.coordinates
