import socket
import time
import operator


# Формат запроса: <команда> <данные запроса><\n>
# <команда>: put, get.


SERVER_RESPONSE_STATUS_OK = 'ok\n\n'
SERVER_RESPONSE_STATUS_ERROR = 'error\nwrong command\n\n'

COMMAND_GET_ALL = '*'


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        self.connection_sock = socket.create_connection((host, port), timeout)

    def put(self, command, metric_value, timestamp=None):
        try:
            timestamp = int(timestamp) if timestamp else int(time.time())
            metric_value = float(metric_value)
        except ValueError as err:
            print('Invalid data format. Error:', err)
            raise ClientError

        msg = 'put' + command + str(metric_value) + str(timestamp) + '\n'
        self.connection_sock.sendall(msg.encode('utf8'))

        response = self.connection_sock.recv(len(SERVER_RESPONSE_STATUS_ERROR))

        if response == SERVER_RESPONSE_STATUS_ERROR:
            raise ClientError

    def get(self, command):
        self.connection_sock.sendall(command.encode('utf8'))

        response = self.connection_sock.recv(4096).decode('utf8')

        if not response:
            raise ClientError

        values_list = response.rstrip('\n').split('\n')[1:]

        data_dict = {}
        for value in values_list:
            metric_value = value.split(' ')

            metric_value[1] = float(metric_value[1])
            metric_value[2] = int(metric_value[2])

            if metric_value[0] not in data_dict:
                data_dict[metric_value[0]] = [(metric_value[2], metric_value[1])]
            else:
                data_dict[metric_value[0]].append((metric_value[2], metric_value[1]))

        for value in data_dict.values():
            sorted(value, key=operator.itemgetter(1))

        return data_dict

    def check_response(self):
        pass

    def close_connection(self):
        self.connection_sock.close()


# if __name__ == '__main__':
#     client = Client('127.0.0.1', 8888)
#     # client.put('hello.cpu', 12)
#     print(client.get('*'))
#     client.close_connection()
