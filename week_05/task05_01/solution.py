import socket
import time
import operator


# Формат запроса: <команда> <данные запроса><\n>
# <команда>: put, get.


SERVER_RESPONSE_STATUS_OK = 'ok\n\n'
SERVER_RESPONSE_STATUS_ERROR = 'error\nwrong command\n\n'

COMMAND_GET_ALL = '*'
COMMANDS = ('get', 'put')


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        try:
            self.connection_sock = socket.create_connection((host, port), timeout)
        except socket.error:
            raise ClientError()

    def read_data(self, buffer_size):
        data = b''

        while not data.endswith(b'\n\n'):
            try:
                data += self.connection_sock.recv(buffer_size)
            except socket.error:
                raise ClientError()

        data = data.decode('utf8')

        if data == SERVER_RESPONSE_STATUS_ERROR:
            raise ClientError()

        return data

    def send_data(self, data):
        # Валидация данных тут!
        try:
            self.connection_sock.sendall(data.encode('utf8'))
        except socket.error:
            print('Error!')

    def put(self, command, metric_value, timestamp=None):
        try:
            timestamp = int(timestamp) if timestamp else int(time.time())
            # metric_value = float(metric_value)
        except ValueError as err:
            print('Invalid data format. Error:', err)
            raise ClientError()

        msg = f'put {command} {str(metric_value)} {str(timestamp)}\n'
        self.send_data(msg)

        response = self.read_data(1024)

        if response == SERVER_RESPONSE_STATUS_ERROR:
            raise ClientError()

    def get(self, value_metric):

        # Формат ответа сервера: <статус ответа><\n><данные ответа><\n\n>

        command = f'get {str(value_metric)}\n'
        self.send_data(command)

        response = self.read_data(1024)

        try:
            values_list = response.rstrip('\n').split('\n')[1:]
        except IndexError:
            raise ClientError()

        data_dict = {}
        for value in values_list:
            metric_value = value.split(' ')

            try:
                metric_value[1] = float(metric_value[1])
                metric_value[2] = int(metric_value[2])
            except (IndexError, ValueError):
                raise ClientError()

            if metric_value[0] not in data_dict:
                data_dict[metric_value[0]] = [(metric_value[2], metric_value[1])]
            else:
                data_dict[metric_value[0]].append((metric_value[2], metric_value[1]))

        for value in data_dict.values():
            value.sort(key=operator.itemgetter(0))

        return data_dict

    @staticmethod
    def check_request_format_client(command: str):
        command_split = command.split(' ')

        if len(command_split) != 4:
            return False
        elif not command_split[3].endswith('\n'):  # check \n
            return False
        elif command_split[0] not in COMMANDS:
            return False

    def close_connection(self):
        self.connection_sock.close()
