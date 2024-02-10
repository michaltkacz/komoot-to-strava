import os

import utils
import config


komoot_tours_list = []
strava_activities_list = []


def check_for_komoot_tours_list():
    if not os.path.exists(config.komoot["tours_list_file_path"]):
        utils.handle_error(f"{config.komoot['tours_list_file_path']} does not exists.")


def check_for_strava_activities_list():
    if os.path.exists(config.strava["activities_list_file_path"]):
        utils.handle_error(
            f"{config.strava['activities_list_file_path']} already exists."
        )


def load_komoot_tours_list():
    global komoot_tours_list
    komoot_tours_list = utils.read_json_file(config.komoot["tours_list_file_path"])


def save_strava_activities_list():
    utils.write_json_file(
        config.strava["activities_list_file_path"], strava_activities_list
    )


def map_komoot_tours_to_strava_activities():
    global strava_activities_list
    try:
        strava_activities_list = list(
            map(
                lambda kt: {
                    "sport_type": config.komoot_to_strava_sport_type_map[kt["sport"]],
                    "name": kt["name"],
                    # "description": "",
                    # "trainer": 0,
                    # "commute": 0,
                    "data_type": "gpx",
                    "external_id": str(kt["id"]),
                },
                komoot_tours_list,
            )
        )
    except Exception as e:
        utils.handle_error("Mapping error.", e)


if __name__ == "__main__":
    utils.log("Running the script...")

    check_for_komoot_tours_list()
    check_for_strava_activities_list()

    utils.log("Mapping Komoot tours list to Strava activities list...")

    check_for_komoot_tours_list()
    load_komoot_tours_list()
    map_komoot_tours_to_strava_activities()
    save_strava_activities_list()

    utils.log("Success. Komoot tours list has been mapped to Strava activites list.")
