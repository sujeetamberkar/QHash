import json
from falcon_lib import falcon
import base64
import os

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

def json_to_string(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return None

    try:
        # Read the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        # Convert the Python dictionary to a string
        data_string = json.dumps(data, indent=4)  # The `indent` parameter is optional, used for pretty-printing
        return data_string

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def signature_process(Json_File_Path):
    normal_string_format = json_to_string(Json_File_Path)
    string_Byte_Format = string_to_bytes(normal_string_format)
    sk = falcon.SecretKey(16)
    pk = falcon.PublicKey(sk)
    signature_Byte_format = sk.sign(string_Byte_Format)
    signature = signature_Byte_format.hex()
    print(pk.verify(a,signature_Byte_format))