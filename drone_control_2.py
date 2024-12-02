from common import *

import socket
import threading
import time

class DroneController:
    """ A class to control a drone using UDP commands. """

    def __init__(self, udp_socket, drone_address):
        """
        Initialize the DroneController.

        Args:
            udp_socket (socket.socket): A pre-configured UDP socket.
            drone_address (tuple): A tuple containing the drone's IP address and port (e.g., ('192.168.1.1', 7099)).
        """
        self.socket = udp_socket
        self.drone_address = drone_address
        self.header = b'\x30\x66'  # Fixed protocol header
        self.footer = b'\x99'  # Fixed protocol footer
        self.running = True

        # Start the listener thread for receiving data
        self.listener_thread = threading.Thread(target=self._listen_for_responses)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def _listen_for_responses(self):
        """
        Continuously listen for responses from the drone.
        """
        print("Listening for drone responses...")
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)  # Adjust buffer size as needed
                # print(f"Received from {addr}: {data.hex()}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error receiving data: {e}")

    def _send_command(self, header_data, primary_state, secondary_state):
        """
        Build and send a command to the drone.

        Args:
            header_data (bytes): 2 bytes for the state header.
            primary_state (bytes): 2 bytes for the primary state.
            secondary_state (bytes): 2 bytes for the secondary state.
        """
        command = self.header + header_data + primary_state + secondary_state + self.footer
        self.socket.sendto(command, self.drone_address)
        print(f"Sent command: {command.hex()} to {self.drone_address}")

    def stop(self):
        """Stop the controller and listener thread."""
        self.running = False

    # Drone control methods (e.g., takeoff, land) remain unchanged
    def takeoff(self):
        print("<<TAKEOFF>>")
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x41\x41')

    def land(self):
        print("<<LAND>>")
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x42\x42')

    def baseline(self):
        print("<<BASELINE>>")
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x40\x40')

# Example usage
if __name__ == "__main__":
    # Configure the UDP socket and drone address
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(2)  # Set a timeout for recvfrom
    udp_socket.bind(('', 0))  # Bind to an available port for two-way communication
    drone_address = ('192.168.1.1', 7099)

    # Initialize the drone controller
    drone_control = DroneController(udp_socket, drone_address)

    # Fly up, stay there for 5 seconds, land
    try:
        drone_control.baseline()
        time.sleep(2)

        ## Magic start command
        u2.sendto(base_start, (DRONE_IP, 53796))

        drone_control.takeoff()
        time.sleep(5)

        drone_control.land()
        time.sleep(2)

        drone_control.baseline()
    finally:
        # Stop the controller and close the socket
        drone_control.stop()
        udp_socket.close()
