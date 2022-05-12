import socket
import threading
import zlib

import mss

WIDTH = 1000
HEIGHT = 600


def retreive_screenshot(conn):

    with mss.mss() as sct:

        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while 'recording':

            img = sct.grab(rect)

            pixels = zlib.compress(img.rgb, 6)

            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))

            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)

            conn.sendall(pixels)


def main(host='0.0.0.0', port=5000):
    with socket.socket() as sock:
        sock.bind((host, port))
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = threading.Thread(target=retreive_screenshot, args=(conn,))
            thread.start()


if __name__ == '__main__':
    import argparse
    import sys

    cli_args = argparse.ArgumentParser()
    cli_args.add_argument('--port', default=5000, type=int)
    options = cli_args.parse_args(sys.argv[1:])

    main(port=options.port)