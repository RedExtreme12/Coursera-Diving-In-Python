import os
import tempfile
import json
import argparse


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
temp = tempfile.mktemp(storage_path)

write_mode = 'w' if not os.path.exists(storage_path) else 'r+'


def get_args():
    """
    We get arguments from terminal.
    :return: None
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-k', '--key', help='key for added in file')
    parser.add_argument('-v', '--value', help='value for added in file')

    args = parser.parse_args()

    return args.key, args.value


def added_key_value(key, value, file, file_size):
    if file_size != 0:
        dictionary = json_to_dict(file)
    else:
        dictionary = dict()

    if key in dictionary:
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

    write_dictionary_to_file(dictionary, file)


def write_dictionary_to_file(_dictionary, file):
    file.seek(0)
    file.write(json.dumps(_dictionary))
    file.write('\n')
    file.truncate()


def json_to_dict(file):
    json_dict = json.load(file)

    return json_dict


def read_key(key, file):
    dictionary = json_to_dict(file)

    if key in dictionary:
        return dictionary[key]


def main(_key, _value):
    if _value:
        with open(storage_path, write_mode) as f:
            size = os.stat(storage_path).st_size
            added_key_value(key, value, f, size)
    else:
        if os.path.exists(storage_path):
            with open(storage_path, 'r') as f:
                values = read_key(_key, f)

                if values:
                    print(', '.join(map(str, values)))


# args.count == 5.
# storage.py --key key_name --val value

if __name__ == '__main__':
    args = get_args()

    key = args[0]
    value = args[1]

    main(key, value)
