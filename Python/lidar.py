import socket
import time
import threading
from flask import Flask

running = False
udp_port = 5044

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
            udp_socket.sendto(bytes(message, 'utf-8'), ('<broadcast>', udp_port))

            count += 1

        time.sleep(0.150)


if __name__ == '__main__':
    udp_thread = threading.Thread(target=udp_thread_function)
    udp_thread.start()

    app.run('0.0.0.0', 8007)
