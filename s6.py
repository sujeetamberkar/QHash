from pymongo import MongoClient

# Connect to your MongoDB cluster
uri = "mongodb+srv://falcon:admin@cluster0.hu0yvct.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

# Select your database and collection
db = client.get_database('yourdbname')  # replace 'yourdbname' with your actual database name
users_collection = db.get_collection('users')  # assumes you have a "users" collection

# The wallet ID you're looking for
target_wallet_id = "e17944be7376ff229cab8fdf307ea0d3339b9c3654836fa98b3e8a58c60249314843f4aaac5b64019641558961fa0fea70023f2affee32cac7d876d5d0165ea4"

# The amount by which to increase the balance
increase_amount = 10  # set to 10 as per your requirement

# Find the user with the specified wallet ID and increase their balance
result = users_collection.update_one(
    {"wallet_ID": target_wallet_id},
    {"$inc": {"balance": increase_amount}}
)

if result.modified_count > 0:
    print("User's balance was successfully updated.")
else:
    print("No user found with the specified wallet ID, or no update was necessary.")
