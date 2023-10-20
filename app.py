from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import dns # required for connecting with SRV
from falcon_lib.falcon import SecretKey, PublicKey
import hashlib
from werkzeug.security import check_password_hash
import json
import random
import datetime
import base64
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
# global_var_sig_1 = 0
# global_var_sig_2 = 0 
# global_var_data_1 = 0
# global_var_data_2 = 0

app = Flask(__name__)

def string_to_bytes(s: str) -> bytes:
    byte_values = []
    parts = s.split('\\x')
    byte_values.extend(parts[0].encode())
    for part in parts[1:]:
        hex_val = part[:2]
        byte_values.append(int(hex_val, 16))
        byte_values.extend(part[2:].encode())
    return bytes(byte_values)

def signature_process():
    with open("transaction_summary.json", "r") as file:
        Transacation_Tranascript = json.load(file)
    data_string = json.dumps(Transacation_Tranascript, indent=4)
    #data_string = data_string.hex()
    byte_format_string =  string_to_bytes(data_string)
    print(f"\n\n{byte_format_string}\n\n")
    
    with open ("session.json", "r") as file:
        user_data = json.load(file)
    with open('user/array.json', 'r') as file:
        poly = json.load(file)

    
    # poly=user_data['secretKey']
    poly = poly
    sk = SecretKey(16,poly)
    signature_Byte = sk.sign(byte_format_string)
    signature = signature_Byte.hex()
    print(f"Signature1 : {signature}")
    # global global_var_sig_1
    # global global_var_data_1
    
    # global_var_sig_1 = signature_Byte
    # global_var_data_1 = byte_format_string
    
    return signature

def verification(signature, public_key_input):
    with open("PublicKeyVerification_Input.json", "r") as file:
        verification_Data = json.load(file)
    
    data_string = json.dumps(verification_Data, indent = 4)
    signature_bytes = bytes.fromhex(signature)
    verification_data_input_byte = string_to_bytes(data_string)
    sk = SecretKey(16)
    pk = PublicKey(sk)

    for i, val in enumerate(public_key_input):
        pk.h[i] = val
        
    global_var_data_2 = verification_data_input_byte
    global_var_sig_2 = signature_bytes
    
    # print(f"\n\nglobal_var_data_2:{global_var_data_2}\n\n")
    # print(f"\n\nglobal_var_data_1:{global_var_data_1}\n\n")
    
    # if global_var_sig_2 == global_var_sig_1:
    #     print("Sig is same")
    # else :
    #     print("Sig is different")
        
    # if global_var_data_1 == global_var_data_2:
    #     print("Data is same")
    # else :
    #     print("Data is different")
        
    check = pk.verify(verification_data_input_byte, signature_bytes)
    if check:
        return "Verification Successful. Payment was done by this public key."
    else:
        return "FALSE. Given Transaction was not done by this public key."
def wrap_string(s, width=30):
    return '\n'.join(s[i:i+width] for i in range(0, len(s), width))

def dict_to_pdf(data, output_filename):
    # Create a bytes buffer to receive the PDF data
    buffer = io.BytesIO()

    # Create a PDF document with the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Styling
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']
    
    # Title of the document
    elems = []
    elems.append(Paragraph('Payment Receipt', style_heading))
    elems.append(Spacer(1, 12))

    # Mapping of data keys to their display labels
    labels = {
        'Transaction_ID': 'Transaction ID',
        'Time_Stamp': 'Time Stamp',
        'Sender_Wallet_ID': 'Sender Wallet ID',
        'Recipient_Wallet_ID': 'Recipient Wallet ID',
        'Amount': 'Amount',
        'Remarks': 'Remarks',
        'Signature': 'Signature'
    }

    # Process the data, wrapping long strings
    for key in ['Sender_Wallet_ID', 'Recipient_Wallet_ID', 'Signature']:
        if key in data:
            data[key] = wrap_string(data[key])

    # Convert the dictionary to a list of lists for ReportLab's Table
    table_data = [['Label', 'Data']]  # Header row
    for key, label in labels.items():
        table_data.append([label, str(data.get(key, ''))])  # get values from data, defaulting to an empty string if key is not found

    # Create a table with the data.
    table = Table(table_data, colWidths=[150, 350], splitByRow=True)

    # Add some style to the table
    table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),  # header row color
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # data row colors
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    elems.append(table)

    # Build the PDF with the elements
    doc.build(elems)

    # Write the PDF to a file
    with open(output_filename, 'wb') as f:
        f.write(buffer.getvalue())

    print(f"Receipt created successfully! Saved as {output_filename}")
def BruteForce(signature):
    with open("Bruteforce_Input.json", "r") as file:
        BruteForce_Data = json.load(file)
    
    data_string = json.dumps(BruteForce_Data, indent=4)
    signature_bytes = string_to_bytes(data_string)  # Convert data_string, not signature
    Brute_Force_input_String = bytes.fromhex(signature)

    for user in users_collection.find():
        public_key_temp = user['PublicKey']
        sk = SecretKey(16)
        pk = PublicKey(sk)

        for i, val in enumerate(public_key_temp):
            pk.h[i] = val

        check = pk.verify(Brute_Force_input_String, signature_bytes)
        if check == True:
            return "Verification Successful. Payment was done by " + user['username']
    return "No Such Payment was made"


# MongoDB connection
uri = "mongodb+srv://falcon:admin@cluster0.hu0yvct.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.get_database('yourdbname') # replace 'yourdbname' with your actual database name
users_collection = db.get_collection('users') # assumes you have a "users" collection

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # check if username already exists
        existing_user = users_collection.find_one({'username': request.form['username']})

        if existing_user is None:
            # For testing purposes, we're keeping the password plain.
            # This is NOT safe for production.
            plain_password = request.form['password']
            sk = SecretKey(16)
            pk = PublicKey(sk)
            poly = sk.get_polynomials()
            get_pk = pk.get_publicKey()
            wallet_ID = CreateWallet_ID(get_pk)
            with open('user/array.json', 'w') as file:
                json.dump(poly, file)


            # insert the user data into the database
            users_collection.insert_one({
                'username': request.form['username'],
                'password': plain_password,  # saving plain password (unsafe)
                # 'secretKey': poly,
                'PublicKey': get_pk,
                'balance': 100,
                'wallet_ID': wallet_ID
            })

            flash('Account created!', category='success')
            return redirect(url_for('login'))
        
        flash('Username already exists!', category='error')

    return render_template('signup.html')

@app.route('/verification-menu')
def verification_menu():
    return render_template('VerificationMenu.html')

@app.route('/verification-input-public-key')
def verification_input_public_key():
    return render_template('Verification_Input_W_PublicKey.html')

@app.route('/process-verification-public-key', methods=['POST'])

def process_verification_public_key():
    # Retrieve form data
    publicKey = request.form.get('publicKey')
    transactionID = request.form.get('transactionID')
    timeStamp = request.form.get('timeStamp')
    senderWalletID = request.form.get('senderWalletID')
    recipientWalletID = request.form.get('recipientWalletID')
    Amount = request.form.get('Amount')  # this is now a string
    Remarks = request.form.get('Remarks')
    signature = request.form.get('signature')

    # Validate that 'amount' is a decimal number
    try:
        # Try to convert the string to a float
        valid_amount = float(Amount)
    except ValueError:
        # 'amount' was not a valid float, redirect back to the form with an error
        flash('Invalid amount. Please enter a numeric value.', 'error')
        return redirect(url_for('verification_input_w_public_key'))  # Adjust this if your route name is different

    # If 'amount' was successfully converted, we can proceed to store it in the dictionary
    Verification_Input_W_PublicKey_DICT = {
        "Transaction_ID": transactionID,
        "Time_Stamp": timeStamp,
        "Sender_Wallet_ID": senderWalletID,
        "Recipient_Wallet_ID": recipientWalletID,
        "Amount": valid_amount,  # store the validated and converted amount
        "Remarks": Remarks
    }

    # Log or print the dictionary and signature for verification purposes
    public_key_input = [int(x.strip()) for x in publicKey.split(',')] # This is as list

    # Store the dictionary in a JSON file
    with open('PublicKeyVerification_Input.json', 'w') as json_file:
        json.dump(Verification_Input_W_PublicKey_DICT, json_file)
    
    verification_result = verification(signature, public_key_input)
    return verification_result

    # Here, you would typically add your logic for the verification process


@app.route('/verification-input-brute-force')
def verification_input_brute_force():
    return render_template('Verification_Input_BruteForce.html')

@app.route('/process-verification-brute-force', methods=['POST'])
def process_verification_brute_force():
    # Retrieve form data
    transactionID = request.form.get('transactionID')
    timeStamp = request.form.get('timeStamp')
    senderWalletID = request.form.get('senderWalletID')
    recipientWalletID = request.form.get('recipientWalletID')
    Amount = request.form.get('Amount')  # this is now a string
    Remarks = request.form.get('Remarks')
    signature = request.form.get('signature')

    # Validate that 'amount' is a decimal number
    try:
        # Try to convert the string to a float
        valid_amount = float(Amount)
    except ValueError:
        # 'amount' was not a valid float, redirect back to the form with an error
        flash('Invalid amount. Please enter a numeric value.', 'error')
        return redirect(url_for('verification_input_brute_force'))
    
    BruteForce_Input_DICT = {
        "Transaction_ID": transactionID,
        "Time_Stamp": timeStamp,
        "Sender_Wallet_ID": senderWalletID,
        "Recipient_Wallet_ID": recipientWalletID,
        "Amount": valid_amount,  # store the validated and converted amount
        "Remarks": Remarks
    }
    with open('Bruteforce_Input.json', 'w') as json_file:
        json.dump(BruteForce_Input_DICT, json_file)



    # ... rest of the method remains the same, using 'valid_amount' for further processing ...
    brute_force_result = BruteForce(signature)
    return brute_force_result




def CreateWallet_ID (int_list):
    result_string = ' '.join(map(str, int_list))
    sha512 = hashlib.sha512()
    sha512.update(result_string.encode('utf-8'))
    hashed_string = sha512.hexdigest()
    return hashed_string

@app.route('/verify-transaction', methods=['POST'])
def verify_transaction():
    # print(1) 
    return redirect(url_for('home'))

@app.route('/make-transaction', methods=['POST'])
def make_transaction():
    return redirect(url_for('login'))  # Redirecting to login page on clicking "Make a Transaction"

@app.route('/validate-login', methods=['POST'])
def validate_login():
    username = request.form.get('username')
    password = request.form.get('password')  # directly get the plain password

    user = users_collection.find_one({'username': username})

    # Just check if the passwords are equal since there's no hashing involved
    if user and user['password'] == password:  # comparing plain-text passwords
        # print(f"Hello {username}")  # Displaying "Hello [Username]" in the terminal

        # Prepare user data to store in session.json
        user_data = {
            "username": user.get("username"),
            "password": user.get("password"),  # Storing plain text password (for testing)
            #"secretKey": user.get("secretKey"),
            "PublicKey": user.get("PublicKey"),
            "balance": user.get("balance"),
            "wallet_ID": user.get("wallet_ID")
        }
        


        # Write data to session.json
        with open("session.json", "w") as file:
            json.dump(user_data, file)

        return render_template('welcome.html', username=user['username'], balance=user['balance'], wallet_ID=user['wallet_ID'], public_key=user['PublicKey'])

    else:
        flash('Invalid username/password', 'error')
        return redirect(url_for('login'))

@app.route('/transaction-input')
def transaction_input():
    with open("session.json", "r") as file:
        user_data = json.load(file)
    return render_template('transactionInput.html', wallet_ID=user_data['wallet_ID'], balance=user_data['balance'])

@app.route('/process-payment', methods=['POST'])
def process_payment():
    # Retrieve form data
    recipient_wallet_id = request.form.get('recipientWalletID')
    Amount = request.form.get('Amount')
    Remarks = request.form.get('Remarks')

    # Read the user data from session.json
    with open("session.json", "r") as file:
        user_data = json.load(file)

    sender_wallet_id = user_data['wallet_ID']
    balance = float(user_data['balance'])  # Assuming balance is stored as a float (or convert from string)

    # Check if balance is sufficient
    Amount = float(Amount)
    if balance < Amount:
        # Redirect back to the payment form with an error message
        return render_template('transactionInput.html', 
                                wallet_ID=sender_wallet_id, 
                                balance=balance, 
                                error="Insufficient funds")


    # If balance is sufficient, proceed with creating the transaction summary
    transaction_ID = generate_random_5_digit_number_as_string()
    transaction_date_time = get_current_time()
    transaction_summary = {
        "Transaction_ID":transaction_ID,
        "Time_Stamp":transaction_date_time,
        "Sender_Wallet_ID": sender_wallet_id,
        "Recipient_Wallet_ID": recipient_wallet_id,
        "Amount": Amount,
        "Remarks": Remarks
    }
    json_file_name = "transaction_summary.json"
    with open(json_file_name, 'w') as json_file:
        json.dump(transaction_summary, json_file)
    Amount = float (Amount)
    # Update the sender's balance
    users_collection.update_one(
        {"wallet_ID": sender_wallet_id},
        {"$inc": {"balance": - Amount}}  # Decrease by 'amount'
    )

    # Update the recipient's balance
    users_collection.update_one(
        {"wallet_ID": recipient_wallet_id},
        {"$inc": {"balance": Amount}}  # Increase by 'amount'
    )

    signature = signature_process()

    Generated_Signature = signature # Will change later
    print(f"Genrate_Signature : {Generated_Signature}")
    payment_reciept_Dict = transaction_summary

    payment_reciept_Dict["signature"] = Generated_Signature

    pdf_parser = transaction_summary
    pdf_parser["Signature"] = Generated_Signature
    filname ="reciept/"+ str(transaction_ID)+".pdf"
    dict_to_pdf(pdf_parser,filname)

    # payment_reciept_json = json.dumps(payment_reciept_Dict)

    # Here you would typically process the payment, e.g., update the database, call a payment API, etc.
    return render_template('paymentReceipt.html', receipt=payment_reciept_Dict)

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
        

def get_current_time():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime
def generate_random_5_digit_number_as_string():
    # Generate a random integer between 10000 and 99999
    random_number = str(random.randint(10000, 99999))
    return random_number


if __name__ == '__main__':
    app.secret_key = 'your_secret'  # Replace 'your_secret' with a real secret key
    app.run(host="0.0.0.0",port=2000,debug=True)




