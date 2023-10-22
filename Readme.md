
# Post-Quantum Banking Platform

Our team Byte Brew Crew took a small step in preparing the world against quantum computers. Due to the rise of Quantum Computers, sooner or later all the traditional cryptographic methods which we use during banking transactions like RSA will be easily breakable.
We came across a new way of making transactions which is quantum-proof

Q-Hash is the first quantum-proof Banking prototype

## Features
### Account Creation
    - 1) Every client will generate a Private Key on his system. Using this private key. The user will generate a Public Key on his system.
    - 2) Using BB84 protocol, a safe way of communication is decided between the user and the server and  a secret key is generated.
    - 3) Now Public key is encrypted using the key generated by the "BB84 protocol" and sent to the server via a secure communication channel
    - 4) The server will push the key, username, and hash(Password) on the database
### Make Transaction 
1. **User Authentication and Interface**: After successful login, users are presented with their current balance, username, and wallet ID. To initiate a transaction, users enter the recipient's username, transaction amount, and remarks.
If the user has sufficient balance we will convert the transaction details into a JSON file and send it to the server.
    
2. **Quantum-Secure Blockchain**:
   - *Quantum Random Number Generation*: Enhancing security through unpredictability, a quantum random number generator produces a truly random number.
   - *Transaction Hashing*: The server generates a SHA3-512 hash value using the received transaction details and the quantum-generated random number.
   - *Blockchain Integration*: Following successful hash generation, the transaction is incorporated into the blockchain.
   - *Receipt and Signature Generation*: Post-transaction, the client's system automatically generates a digital signature using the client's private key and produces a PDF receipt.


### Verification 
   - *Receipt-Based Verification*: Transactions can be independently verified using the generated receipt and the sender's public key, without requiring login.
   - *Result*: The verification process returns a simple True or False response.
### Business Model
1. **Premium Transaction Threshold**: Given the high operational costs associated with quantum computing, Q-Hash is currently positioned as a premium service for transactions exceeding Rs 75,000.
   
2. **Revenue Generation**: The platform sustains its revolutionary service by levying a 1% fee on each transaction processed.
   
3. **Target Demographics**: Q-Hash is ideal for high-stake transactions demanding utmost security and transparency, such as:
   - Government contracts
   - Arms dealings
   - High-end luxury purchases


## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/sujeetamberkar/QHash
```

Navigate to the project directory and install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Flask application:

```bash
python app.py
```

Access the application in your web browser at `http://127.0.0.1:5000/`.

## Pages

- `home.html`: Landing page welcoming users to the post-quantum banking platform.
- `login.html`: Login interface for existing users.
- `signup.html`: Registration page for new users.
- `VerificationMenu.html`: Allows users to choose a verification method.
- `Verification_Input_BruteForce.html`: Interface for verifying transactions using brute force.
- `Verification_Input_W_PublicKey.html`: Interface for verifying transactions with a public key.
- `welcome.html`: Personalized user welcome page.
- `transactionInput.html`: A form for processing new transactions.
- `paymentReceipt.html`: Displays transaction receipts.

## Authors
- [Sujeet Amberkar](https://www.linkedin.com/in/sujeet-amberkar-40b2021b4/?originalSubdomain=in)
- [Utkarsh Dubey](https://github.com/Utkarsh0Dubey)
- [Adithi Bhat](https://www.linkedin.com/in/adithi-bhat-472b3b1b1/)
- [Rashi Gokharu](https://www.linkedin.com/in/rashi-gokharu-a5069625b/)
