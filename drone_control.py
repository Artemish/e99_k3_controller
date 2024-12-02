from common import *
import socket

class DroneController:
    """
    A class to control a drone using UDP commands.
    """

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
        self.socket.recvfrom(1024)
        print(f"Sent command: {command.hex()} to {self.drone_address}")

    def takeoff(self):
        """Send the takeoff command."""

        print('<<TAKEOFF>>')
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x41\x41')

    def land(self):
        """Send the landing command."""

        print('<<LAND>>')
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x42\x42')

    def emergency_stop(self):
        """Send the emergency stop command."""

        print('<<STOP>>')
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x44\x44')

    def headless_mode_on(self):
        """Enable headless mode."""

        print('<<HEADLESS_ON>>')
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x50\x50')

    def headless_mode_off(self):
        """Disable headless mode."""

        print('<<HEADLESS_OFF>>')
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x40\x40')

    def calibrate(self):
        """Send the calibration command."""

        print('<<CALIBRATE>>')
        self._send_command(b'\x80\x80', b'\x80\x80', b'\xC0\xC0')

    def throttle_up(self, increment):
        """Increase throttle."""

        print('<<THROTTLE_UP>>')
        primary_state = (0x80 + increment).to_bytes(2, 'big')
        self._send_command(b'\x80\x80', primary_state, b'\x40\x40')

    def throttle_down(self, decrement):
        """Decrease throttle."""

        print('<<THROTTLE_DOWN>>')
        primary_state = (0x80 - decrement).to_bytes(2, 'big')
        self._send_command(b'\x80\x80', primary_state, b'\x40\x40')

    def rotate_left(self, speed):
        """Rotate the drone left."""

        print('<<ROTATE_LEFT>>')
        primary_state = (0x7B + speed).to_bytes(2, 'big')
        self._send_command(b'\x80\x80', primary_state, b'\x40\x7D')

    def rotate_right(self, speed):
        """Rotate the drone right."""

        print('<<ROTATE_RIGHT>>')
        primary_state = (0x74 + speed).to_bytes(2, 'big')
        self._send_command(b'\x80\x80', primary_state, b'\x40\x85')

    def baseline(self):
        """Send the baseline state command."""

        print('<<BASELINE>>')
        self._send_command(b'\x80\x80', b'\x80\x80', b'\x40\x40')

# Example usage
if __name__ == "__main__":
    # Configure the UDP socket and drone address
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    u2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    drone_address = (DRONE_IP, DRONE_CONTROL_PORT)

    # Initialize the drone controller
    drone_control = DroneController(udp_socket, drone_address)

    
    import time
    base_start = str_to_bytes("800000000000000000000000")
    all_green = str_to_bytes("0101")
    unknown = str_to_bytes("ef000400")


    print("Sending magic string..")
    u2.sendto(unknown, ('192.168.168.1', 8800))
    time.sleep(2)

    print("Base start..")
    udp_socket.sendto(base_start, (DRONE_IP, 53796))
    time.sleep(1)
    print("All green..")
    udp_socket.sendto(all_green, drone_address)
    time.sleep(3)

    # Example commands
    drone_control.baseline()
    time.sleep(10)

    drone_control.takeoff()
    time.sleep(1)
    drone_control.baseline()
    time.sleep(1)
    drone_control.land()
    time.sleep(1)
    drone_control.baseline()
