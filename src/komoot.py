import requests
import sys
import time
import json
import os


"""
    LINKS
"""
tours_url = "https://www.komoot.com/api/v007/users/{}/tours"
tours_url_params = "/?sport_types=&type=tour_recorded&sort_field=date&sort_direction=desc&status=public&page={}&limit={}"
gpx_url = "https://www.komoot.com/api/v007/tours/{}.gpx"


"""
    CONFIG
    * user_id - your komoot user ID
"""
user_id = 0  # your user ID here - integer


"""
    FUNCTIONS
"""


def get_tours(current_page_index=0, current_page_limit=25):
    print("<< --- GET TOURS INFO ---")
    tours = []
    while True:
        url = tours_url.format(user_id) + tours_url_params.format(
            current_page_index, current_page_limit
        )

        print("<< Sending request...")
        response = requests.get(url)
        if not response.ok:
            print("<< Bad response. Program will exit")
            sys.exit()

        print("<< Response OK. Processing data...")
        current_page_content = response.json()
        current_page_tours = map(
            lambda tour: {
                "id": tour.get("id", None),
                "status": tour.get("status", None),
                "date": tour.get("date", None),
                "name": tour.get("name", None),
                "distance": tour.get("distance", None),
                "duration": tour.get("duration", None),
                "sport": tour.get("sport", None),
                "start_point": tour.get("start_point", None),
                "elevation_up": tour.get("elevation_up", None),
                "elevation_down": tour.get("elevation_down", None),
                "time_in_motion": tour.get("time_in_motion", None),
                "changed_at": tour.get("changed_at", None),
            },
            current_page_content["_embedded"]["tours"],
        )
        tours.extend(list(current_page_tours))

        total_pages = current_page_content["page"]["totalPages"]
        total_items = current_page_content["page"]["totalElements"]

        print(
            "<< Status: fetched {} out of {} tours".format(
                (current_page_index + 1) * current_page_limit, total_items
            )
        )

        current_page_index += 1
        if current_page_index >= total_pages:
            print("<< Fetching is done")
            break

    return tours


def get_gpx(tour_id):
    print("<< --- GET TOUR GPX {} ---".format(tour_id))
    print("<< Sending request...")
    response = requests.get(gpx_url.format(tour_id))
    if not response.ok:
        print("<< Bad response. Program will exit")
        sys.exit()
    print("<< Response OK. Processing data...")
    return response.text


def save_to_file(tours):
    def is_already_saved(tour_id):
        print("<< --- IS ALREADY SAVED {}".format(tour_id))
        existing_files = os.listdir("./gpx")
        for file in existing_files:
            if "{}".format(tour_id) in file:
                return True
        return False

    print("<< --- SAVE TO FILE ---")
    print("<< Saving tours...")
    open("./gpx/tours.json", "w", encoding="utf-8").write(json.dumps(tours))
    print("<< Tours saved")

    for tour in tours:
        id = tour["id"]
        if is_already_saved(id):
            print("<< GPX already saved. Skipping to next tour")
            continue

        print("<< GPX has to be downloaded and saved")
        gpx = get_gpx(id)
        print("<< Saving gpx...")
        open("./gpx/" + str(id) + ".gpx", "w", encoding="utf-8").write(gpx)
        print("<< GPX saved")
        time.sleep(1)

    print("<< Success. All data has been saved")


"""
    MAIN
"""
if __name__ == "__main__":
    tours = get_tours()
    save_to_file(tours)
