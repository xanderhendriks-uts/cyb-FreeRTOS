"""
This script sniffs for UDP packets and prints them to stdout

Example usage:

.. code-block:: python

    udp_sniffer.py
"""
import argparse
import socket


def main():
    """
    Main function

    """
    parser = argparse.ArgumentParser(description='Sniff for UDP packets on the given port and print them to stdout')
    options = parser.parse_args()

    udp_port = 5044

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Listening on: %d" % udp_port)

    udp_socket.bind(('', udp_port))

    while True:
        message, address = udp_socket.recvfrom(409600)
        print(message.decode('utf-8'))


if __name__ == '__main__':
    main()
