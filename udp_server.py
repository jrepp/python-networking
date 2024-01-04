import socket
import json
from log_message import LogMessage

def udp_server():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    print(f"UDP server listening on {server_address}")

    while True:
        # Receive the data and client address
        data, client_address = server_socket.recvfrom(1024)

        # Deserialize the received data
        try:
            received_log_message = LogMessage.from_bytes_with_header(data)
            print(f"Received LogMessage from {client_address}: {received_log_message}")
            # Process the received LogMessage (modify or respond as needed)
            response_message = f"Server received: {received_log_message.message}"
        except AttributeError as e_attr:
            print(f"AttributeError: {e_attr}")
            response_message = "Failed to call from_bytes_with_header on data"
        except json.JSONDecodeError as e_json:
            print(f"Failed to deserialize the received JSON data: {e_json}")
            response_message = "Failed to process the received LogMessage"
        
        # Send the response without encoding to bytes
        server_socket.sendto(response_message.encode(), client_address)

# Run the UDP server
if __name__ == '__main__':
    udp_server()
