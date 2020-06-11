"""
This script sniffs for UDP packets and prints them to stdout

Example usage:

.. code-block:: python

    udp_sniffer.py
"""
import argparse
import requests


ip_address = 'localhost'

def main():
    """
    Main function

    """
    parser = argparse.ArgumentParser(description='Sniff for UDP packets on the given port and print them to stdout')
    options = parser.parse_args()

    # Get the secret for the pointcloud packet authentication
    response = requests.get('https://%s:8007/mode/set/run' % ip_address, verify=False, cert=('client.crt', 'client.key'))
    print (response.text)


if __name__ == '__main__':
    main()
