import os
import time
import json
import sys

import config


def is_dir_exist(dir_path):
    return os.path.exists(dir_path)


def is_file_exist(dir_path, file_name, file_extension):
    if not is_dir_exist(dir_path):
        return False

    files_in_dir = os.listdir(dir_path)
    for file in files_in_dir:
        if str(file_name + file_extension) in file:
            return True
    return False


def build_file_path(dir_path, file_name, file_extension):
    return dir_path + file_name + file_extension


def build_safe_file_path(dir_path, file_name, file_extension):
    make_dir_if_not_exist(dir_path)
    return get_first_unique_file_path(dir_path, file_name, file_extension)


def get_first_unique_file_path(dir_path, file_name, file_extension):
    path_args = (dir_path, file_name, file_extension)
    is_file_already_exist = is_file_exist(*path_args)

    index = 1
    while is_file_already_exist:
        path_args = (
            dir_path,
            file_name + config.common["file_name_safe_separator"] + str(index),
            file_extension,
        )
        is_file_already_exist = is_file_exist(*path_args)
        index += 1

    return build_file_path(*path_args)


def make_dir_if_not_exist(dir_path):
    if not is_dir_exist(dir_path):
        os.mkdir(dir_path)


def get_nested(obj, keys, default=None):
    try:
        for key in keys:
            obj = obj[key]
        return obj
    except (KeyError, TypeError):
        return default


def write_json_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)


def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data


def write_text_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as gpx_file:
        gpx_file.write(data)


def throttle_requests():
    time.sleep(1)


def handle_request_error():
    print("Bad request. Script will terminate.")
    exit()


def exit():
    sys.exit()
