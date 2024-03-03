# Cat API Websocket, Diego gosmar

import sys
import cheshire_cat_api as ccat
import time

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

print("CAT URL:", cat_url)

def on_open():
    # This is triggered when the connection is opened
    print("Connection opened!")

def on_message(message: str):
    # This is triggered when a new message arrives
    # and grabs the message
    print(message)

def on_error(exception: Exception):
    # This is triggered when a WebSocket error is raised
    print(str(exception))

def on_close(status_code: int, message: str):
    # This is triggered when the connection is closed
    print(f"Connection closed with code {status_code}: {message}")

# Connection settings with default values
config = ccat.Config(
    base_url=cat_url,
    port=1865,
    user_id="user",
    auth_key=auth_key,
    secure_connection=False
)

# Cat Client
cat_client = ccat.CatClient(
    config=config,
    on_open=on_open,
    on_close=on_close,
    on_message=on_message,
    on_error=on_error
)

# Connect to the WebSocket API
cat_client.connect_ws()

while not cat_client.is_ws_connected:
    # A better handling is strongly advised to avoid an infinite loop
    time.sleep(1)

# Check if a message argument is provided
if len(sys.argv) > 1:
    message_to_send = sys.argv[1]
else:
    message_to_send = "Hello Cat!"  # Default message

# Send the message
cat_client.send(message=message_to_send)

# Wait for a response (e.g., 5 seconds)
time.sleep(20)

# Close connection
cat_client.close()
