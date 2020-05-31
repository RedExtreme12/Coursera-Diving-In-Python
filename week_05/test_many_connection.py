import socket
import threading
import multiprocessing

WORKERS_COUNT = 3


def worker():
    while True:
        conn, addr = sock.accept()

        th = threading.Thread(target=process_request, args=(conn, addr))
        th.start()


def process_request(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode('utf8'))


# In main we create new process with threads.
if __name__ == '__main__':
    with socket.socket() as sock:
        sock.bind(('', 10001))
        sock.listen()

        workers_list = [multiprocessing.Process(target=worker, args=(sock,)) for _ in range(WORKERS_COUNT)]

        for w in workers_list:
            w.start()

        for w in workers_list:
            w.join()
