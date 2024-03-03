# Cat API Websocket and REST, Diego gosmar

from flask import Flask, request, jsonify
import threading
import cheshire_cat_api as ccat
import time
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Read AUTH_KEY from a file
def read_auth_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

auth_key_file_path = '../auth_key.txt'  # Replace with your file path
auth_key = read_auth_key(auth_key_file_path)

# Read CATURL from a file
def read_cat_url(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

auth_cat_url_path = '../cat_url.txt'  # Replace with your file path
cat_url = read_auth_key(auth_cat_url_path)

def read_expected_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

expected_api_key_file_path = '../expected_api_key.txt'  # Replace with your file path
EXPECTED_API_KEY = read_expected_api_key(expected_api_key_file_path)

app = Flask(__name__)

# Global list to store messages from WebSocket
messages = []

def on_open():
    print("Connection opened!")

def on_message(message: str):
    print(message)
    messages.append(message)  # Append each message to the global list

def on_error(exception: Exception):
    print(str(exception))

def on_close(status_code: int, message: str):
    print(f"Connection closed with code {status_code}: {message}")

@app.route('/sendMessage', methods=['POST'])
def send_message():
    print(request.headers)
    # Check for API Key in the request headers
    api_key = request.headers.get('Apikey')
    print("Expected API Key",EXPECTED_API_KEY)
    print("Received API Key",api_key)

    if api_key != EXPECTED_API_KEY:
        return jsonify({"error": "Invalid or missing API Key"}), 401

    data = request.json
    message_to_send = data.get('message', 'Hello Cat!')

    # Clear previous messages
    messages.clear()

    def handle_websocket():
        config = ccat.Config(
            base_url=cat_url,
            port=1865,
            user_id="user",
            auth_key=auth_key,
         #   auth_key="",
            secure_connection=False
        )

        cat_client = ccat.CatClient(
            config=config,
            on_open=on_open,
            on_close=on_close,
            on_message=on_message,
            on_error=on_error
        )

        cat_client.connect_ws()
        while not cat_client.is_ws_connected:
            time.sleep(1)
        print("Using API Key:", auth_key)
        cat_client.send(message=message_to_send)
        time.sleep(12)  # Adjust this as needed
        cat_client.close()

    # Run the WebSocket communication in a separate thread
    thread = threading.Thread(target=handle_websocket)
    thread.start()
    thread.join()

    return jsonify({"status": "Message sent", "replies": messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
