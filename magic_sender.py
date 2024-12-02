#!/usr/bin/env python3

from common import *

import socket
import time
import threading

# Configuration
MAGIC_MSG = str_to_bytes("ef000400")
INTERVAL = 0.10

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

    print('Transmitting..', end='', flush=True)
    try:
        while True:
            sock.sendto(MAGIC_MSG, ('192.168.169.1', 8800))
            print('.', end='', flush=True)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nShutting down.")
        sock.close()


if __name__ == "__main__":
    main()
