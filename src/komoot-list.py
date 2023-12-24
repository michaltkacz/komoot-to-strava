import requests

import utils
import config


def get_tours_list():
    url = config["komoot.first_page_url"]
    tours_list = []
    while url:
        page = fetch_page(url)
        new_tours, next_page_url = get_tours_list_from_page(page)
        tours_list.extend(list(new_tours))
        url = next_page_url
        utils.throttle_requests()

    return tours_list


def fetch_page(page_url):
    try:
        return requests.get(page_url).json()
    except:
        utils.handle_request_error()


def get_tours_list_from_page(page):
    page_tours_list = map(
        lambda tour: {
            wanted_key: tour.get(wanted_key, None)
            for wanted_key in config.komoot["wanted_keys"]
        },
        page["_embedded"]["tours"],
    )
    next_page_url = utils.get_nested(page, ["_links", "next", "href"])
    return [page_tours_list, next_page_url]


def save_tours_list(tours_list):
    path_args = (
        config.common["tours_data_directory"],
        config.common["tours_list_file_name"],
        config.common["tours_list_file_extension"],
    )
    file_path = utils.build_safe_file_path(*path_args)
    utils.write_json_file(file_path, tours_list)


"""
    MAIN
"""
if __name__ == "__main__":
    print("### Fetching tours list...")

    tours_list = get_tours_list()
    save_tours_list(tours_list)

    print(f"### Saved list of {len(tours_list)} tours")
