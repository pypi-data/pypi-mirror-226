import json


def write_file(file_path: str, string: str):
    with open(file_path, "w") as file:
        file.write(string)


def read_file(file_path: str):
    with open(file_path, "r") as file:
        return file.read()


def write_json(file_path: str, data_structure):
    with open(file_path, "w") as file:
        json.dump(data_structure, file)


def read_json(file_path: str):
    with open(file_path, "r") as file:
        return json.load(file)
