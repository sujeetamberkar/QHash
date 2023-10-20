import json
from falcon_lib import falcon
import base64
from pymongo import MongoClient


uri = "mongodb+srv://falcon:admin@cluster0.hu0yvct.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database('yourdbname') # replace 'yourdbname' with your actual database name
users_collection = db.get_collection('users') # assumes you have a "users" collection

def string_to_bytes(s: str) -> bytes:
    byte_values = []
    # Split the string on the '\\x' delimiter
    parts = s.split('\\x')
    # The first part is taken as direct characters
    byte_values.extend(parts[0].encode())
    # For the remaining parts...
    for part in parts[1:]:
        # The first two characters should be the hex representation
        hex_val = part[:2]
        byte_values.append(int(hex_val, 16))
        # Any remaining characters in the part are taken as direct characters
        byte_values.extend(part[2:].encode())
    return bytes(byte_values)

def BruteForce(signature):
    with open("Bruteforce_Input.json", "r") as file:
        BruteForce_Data = json.load(file)
    
    data_string = json.dumps(BruteForce_Data, indent=4)
    signature_bytes = string_to_bytes(data_string)
    Brute_Force_input_String = bytes.fromhex(signature)
    for user in users_collection.find():
        public_ket_temp = user ['PublicKey']
        sk = falcon.SecretKey(16)
        pk = falcon.PublicKey(sk)
        for i,val in enumerate (public_ket_temp):
            pk.h[i]=val
        check = pk.verify(Brute_Force_input_String,signature_bytes)
        if check == True:
            return  "Verification Sucessfull Payment was done by ",user['username'],
        else :
            return "No Such Payment was made"
        

def verification(signature,public_key_input):
    with open("PublicKeyVerification_Input", "r") as file:
        verification_Data = json.load(file)
    data_string = json.dumps(verification_Data, indent=4)
    signature_bytes = bytes.fromhex(signature)
    verification_data_input_byte = string_to_bytes(signature_bytes)
    sk = SecretKey(16)
    pk = PublicKey(sk)

    for i,val in enumerate (public_key_input):
            pk.h[i]=val
    check = pk.verify(verification_data_input_byte,signature_bytes)
    if check == True:
        return  "Verification Sucessfull Payment was done by this public key "
    else :
        return "FALSE Given Transacation was not done by this public key"


    


