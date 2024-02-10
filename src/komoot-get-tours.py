import requests
import os

import utils
import config


tours_list = []


def check_for_tours_list():
    if os.path.exists(config.komoot["tours_list_file_path"]):
        utils.handle_error(f"{config.komoot['tours_list_file_path']} already exists.")


def get_tours_list():
    url = config.komoot["first_tours_lists_page_url"]
    try:
        while url:
            page = requests.get(url).json()

            new_tours = []
            if config.komoot["save_only_wanted_keys"]:
                new_tours = map(
                    lambda tour: {
                        wanted_key: tour.get(wanted_key, None)
                        for wanted_key in config.komoot["wanted_keys"]
                    },
                    page["_embedded"]["tours"],
                )
            else:
                new_tours = utils.get_nested(page, ["_embedded", "tours"])

            url = utils.get_nested(page, ["_links", "next", "href"])
            tours_list.extend(list(new_tours))
            utils.throttle_requests()
    except Exception as e:
        utils.handle_error("Request error.", e)


def save_tours_list():
    check_for_tours_list()
    utils.write_json_file(config.komoot["tours_list_file_path"], tours_list)


if __name__ == "__main__":
    utils.log("Running the script...")

    check_for_tours_list()

    utils.log("Fetching tours list...")

    get_tours_list()
    save_tours_list()

    utils.log(f"Saved list of {len(tours_list)} Komoot tours.")
