"""
This script sniffs for UDP packets and prints them to stdout

Example usage:

.. code-block:: python

    udp_sniffer.py
"""
import argparse
import hmac
import hashlib
import requests
import socket

ip_address = 'localhost'

def main():
    """
    Main function

    """
    parser = argparse.ArgumentParser(description='Sniff for UDP packets on the given port and print them to stdout')
    options = parser.parse_args()

    # Get the secret for the pointcloud packet authentication
    response = requests.get('https://%s:8007/secret/get' % ip_address, verify=False, cert=('client.crt', 'client.key'))
    print (response.text)

    api_secret = response.json()['secret']
    udp_port = 5044

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Listening on: %d" % udp_port)

    udp_socket.bind(('', udp_port))

    while True:
        message, address = udp_socket.recvfrom(409600)
        
        signature = hmac.new(bytes(api_secret , 'utf-8'), msg=message[:-64], digestmod=hashlib.sha256).hexdigest().upper()
        
        if signature == message[-64:].decode('utf-8'):
            print(message[:-64].decode('utf-8'))
        else:
            print("Authentication failed: %s" % message.decode('utf-8'))


if __name__ == '__main__':
    main()
