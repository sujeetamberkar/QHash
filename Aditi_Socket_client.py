import socket
import json
import os

def send_json_to_server(host, port, file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Read the JSON file's contents
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        print(f"Failed to read and parse JSON file: {e}")
        return

    # Convert the JSON data back to a string to send
    json_string = json.dumps(json_data)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))

        # Send the JSON data as a string
        client_socket.sendall(json_string.encode('utf-8'))
    except Exception as e:
        print(f"Failed to send data: {e}")
    finally:
        # Close the socket
        client_socket.close()

if __name__ == "__main__":
    # You need to know the server's IP address and port. Replace 'localhost' and 12345 with the appropriate values.
    HOST = '172.20.10.9'  # The server's hostname or IP address
    PORT = 34709        # The port used by the server
    FILE_PATH = 'transaction_summary.json'

    send_json_to_server(HOST, PORT, FILE_PATH)
