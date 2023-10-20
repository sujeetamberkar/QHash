from pymongo import MongoClient
import hashlib
import random
import datetime
import json


def generate_random_5_digit_number_as_string():
    # Generate a random integer between 10000 and 99999
    random_number = str(random.randint(10000, 99999))
    return random_number

# Example usage:
random_number_str = generate_random_5_digit_number_as_string()
print("Random 5-Digit Number as a String:", random_number_str)

def CreateWallet_ID (int_list):
    result_string = ' '.join(map(str, int_list))
    sha512 = hashlib.sha512()
    sha512.update(result_string.encode('utf-8'))
    hashed_string = sha512.hexdigest()
    return hashed_string

def get_current_time():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime


print(generate_random_5_digit_number_as_string())


# uri = "mongodb+srv://falcon:admin@cluster0.hu0yvct.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri)
# db = client.get_database('yourdbname') # replace 'yourdbname' with your actual database name
# users_collection = db.get_collection('users') # assumes you have a "users" collection


# for user in users_collection.find():
#     a=user

# b=a['PublicKey']

# transaction_ID = random.random()
# current_datetime = get_current_time()
# sender_Wallet_ID = getWallet_ID(b)
# receiver_Wallet_ID = getWallet_ID(b)
# amount = 1000
# remark = "Test"


# transaction_data = {
#     "transaction_ID": transaction_ID,
#     "current_datetime": current_datetime,
#     "sender_Wallet_ID": sender_Wallet_ID,
#     "receiver_Wallet_ID": receiver_Wallet_ID,
#     "amount": amount,
#     "remark": remark
# }


# json_file_name = "data.json"
# with open(json_file_name, 'w') as json_file:
#     json.dump(transaction_data, json_file)









