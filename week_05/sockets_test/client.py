import socket


if __name__ == '__main__':
    with socket.create_connection(('127.0.0.1', 10001), 5) as sock:
        sock.settimeout(2)
