import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)

db = client['foo-app']

session = db.session
track = db.track
