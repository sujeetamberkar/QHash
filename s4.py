import json
from falcon_lib import falcon
from pymongo import MongoClient


with open ("session.json", "r") as file:
    user_data = json.load(file)

uri = "mongodb+srv://falcon:admin@cluster0.hu0yvct.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database('yourdbname') # replace 'yourdbname' with your actual database name
users_collection = db.get_collection('users') # assumes you have a "users" collection


message = "sujeet"
signature = "sig"
for user in users_collection.find():
    print(i['PublicKey'])
    sk = falcon.SecretKey(16)
    pk = falcon.PublicKey(sk)
    get_Public_key = pk.get_publicKey()
    for i,val in enumerate (get_Public_key):
        pk.h[i]=val
    check = pk.verify(message,signature)
    if check == True:
        print(user)
    else :
        print("No such transacation was ever made")