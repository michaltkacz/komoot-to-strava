import time
import json
import sys
from datetime import datetime

import config


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


def throttle_requests(seconds=1):
    time.sleep(seconds)


def log(*values):
    if config.common["enable_logs"]:
        timestamp = datetime.now() if config.common["enable_logs_timestamp"] else ""
        print("###", timestamp, *values)


def handle_error(*values):
    log("Error. Script terminated.")
    if values:
        log("Reason: ", *values)
    sys.exit()
