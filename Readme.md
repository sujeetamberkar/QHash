
# Post-Quantum Banking Platform

This project is a prototype of a banking platform designed with post-quantum security algorithms. It features a user-friendly interface for common banking operations and integrates advanced security verification methods.

## Features

- User Authentication: Secure login and signup pages.
- Transaction Processing: Interface for inputting transaction details and viewing payment receipts.
- Advanced Verification: Options to verify transactions using brute force or public key methods, showcasing the application's readiness for post-quantum security challenges.

## Installation

Clone the repository to your local machine:

```bash
git clone <repository-url>
```

Navigate to the project directory and install the dependencies:

```bash
cd <project-directory>
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

## Contributing

Contributions are welcome. Please fork the repository and create a pull request with your changes.

## License

Specify your project's license here.
