#!/usr/bin/env python3

import socket
import time
import threading

# Configuration
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 7099     # Port to listen on
RESPONSE_PAYLOAD = b'\x48\x02\x00\x00\x00'
RESPONSE_INTERVAL = 0.05  # Interval in seconds between responses

# Global variable to store client address
client_address = None

def listen_for_data(sock):
    """
    Thread to listen for incoming UDP datagrams.
    """
    global client_address
    last_message = None
    print(f"Listening on UDP port {UDP_PORT}...")
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        # print(f"Received message: {data} from {addr}")
        client_address = addr  # Update client address for responses
        if len(data) != 9:
            continue

        if data != last_message:
            print(f'DATA: {data.hex()}')
            last_message = data


def send_responses(sock):
    """
    Thread to send periodic responses to the last known client address.
    """
    global client_address
    while True:
        if client_address:
            sock.sendto(RESPONSE_PAYLOAD, client_address)
            # print(f"Sent payload: {RESPONSE_PAYLOAD} to {client_address}")
        time.sleep(RESPONSE_INTERVAL)  # Wait before sending the next response


def main():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    # Start threads for reading and writing
    listener_thread = threading.Thread(target=listen_for_data, args=(sock,))
    sender_thread = threading.Thread(target=send_responses, args=(sock,))
    
    listener_thread.daemon = True  # Allow program to exit even if thread is running
    sender_thread.daemon = True

    listener_thread.start()
    sender_thread.start()

    try:
        while True:  # Keep the main thread alive
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down.")
        sock.close()


if __name__ == "__main__":
    main()
