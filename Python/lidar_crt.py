import hmac
import hashlib
import secrets
import socket
import ssl
import time
import threading
from flask import Flask

running = False
udp_port = 5044
api_secret = secrets.token_hex(20)

app = Flask(__name__)

@app.route('/mode/set/<mode>')
def mode_set(mode):
    global running

    if mode.lower() == 'run':
        running = True
        reply_string = '{"status": "%s"}' % "Running" if running else "Idle"
    elif mode.lower() == 'idle':
        running = False
        reply_string = '{"status": "%s"}' % "Running" if running else "Idle"
    else:
        reply_string = '{"error": "Invalid mode"}'
    
    return reply_string


@app.route('/mode/get')
def mode_get():
    return '{"status": "%s"}' % "Running" if running else "Idle"


@app.route('/secret/get')
def secret_get():
    return '{"secret": "%s"}' % api_secret


@app.route('/secret/reset')
def secret_reset():
    global api_secret

    api_secret = secrets.token_hex(20)
    return '{"secret": "%s"}' % api_secret


@app.errorhandler(404) 
def not_found(e): 
    return '{"error": "Invalid command"}'


def udp_thread_function():
    # Setup the UDP socket for broadcasting the pointcloud packets
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    print("Broadcasting on: %d" % udp_port)

    count = 0

    while True:
        if running:
            message = 'Real LiDAR Pointcloud packet: Message number %d' % count
            signature = hmac.new(bytes(api_secret , 'utf-8'), msg = bytes(message , 'utf-8'), digestmod = hashlib.sha256).hexdigest().upper()
            udp_socket.sendto(bytes(message + signature, 'utf-8'), ('<broadcast>', udp_port))

            count += 1

        time.sleep(0.150)


if __name__ == '__main__':
    udp_thread = threading.Thread(target=udp_thread_function)
    udp_thread.start()

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('ca-crt.pem')
    context.load_cert_chain('server.crt', 'server.key')
    app.run('0.0.0.0', 8007, ssl_context=context)
