import requests

import utils
import config


def load_tours_list():
    path_args = (
        config.common["tours_data_directory"],
        config.common["tours_list_file_name"],
        config.common["tours_list_file_extension"],
    )
    file_path = utils.build_file_path(*path_args)
    return utils.read_json_file(file_path)


def save_tours_gpx(tours_list):
    for tour in tours_list:
        save_tour_gpx_if_need(tour["id"])


def save_tour_gpx_if_need(tour_id):
    path_args = (
        config.common["tours_data_directory"],
        str(tour_id),
        config.common["gpx_file_extension"],
    )

    if utils.is_file_exist(*path_args):
        print(f"{tour_id} is already saved.")
    else:
        print(f"{tour_id} downloading...")
        file_path = utils.build_safe_file_path(*path_args)
        tour_gpx = get_tour_gpx(tour_id)
        utils.write_text_file(file_path, tour_gpx)
        utils.throttle_requests()


def get_tour_gpx(tour_id):
    try:
        url = config.komoot["gpx_file_url"].format(tour_id)
        return requests.get(url).text
    except:
        utils.handle_request_error()


"""
    MAIN
"""
if __name__ == "__main__":
    print("### Fetching tours gpx...")

    tours_list = load_tours_list()
    save_tours_gpx(tours_list)

    print("### Success. All data has been saved.")
