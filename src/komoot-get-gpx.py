import requests
import os

import utils
import config


tours_list = []


def check_for_tours_list():
    if not os.path.exists(config.komoot["tours_list_file_path"]):
        utils.handle_error(f"{config.komoot['tours_list_file_path']} does not exists.")


def load_tours_list():
    global tours_list
    tours_list = utils.read_json_file(config.komoot["tours_list_file_path"])


def save_tours_gpx():
    try:
        for index, tour in enumerate(tours_list):
            tour_gpx_file_path = config.common["gpx_file_path"].format(tour["id"])
            tour_gpx_url = config.komoot["gpx_file_url"].format(tour["id"])

            if os.path.exists(tour_gpx_file_path):
                utils.log(
                    f"[{index + 1}/{len(tours_list)}] ID: '{tour['id']}' Name: '{tour['name']}' is already saved. Skipping."
                )
            else:
                tour_gpx = requests.get(tour_gpx_url).text
                utils.write_text_file(tour_gpx_file_path, tour_gpx)
                utils.log(
                    f"[{index + 1}/{len(tours_list)}] ID: '{tour['id']}' Name: '{tour['name']}' saved."
                )
                utils.throttle_requests()
    except Exception as e:
        utils.handle_error("An unexpected error occured.", e)


if __name__ == "__main__":
    utils.log("Running the script...")

    check_for_tours_list()

    utils.log("Fetching tours GPX files from Komoot...")

    load_tours_list()
    save_tours_gpx()

    utils.log("Success. Komoot tours data has been downloaded and saved.")
