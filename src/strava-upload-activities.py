import requests
import urllib3
import os

import utils
import config

"""
    Quickfix for:
    InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.strava.com'. 
    Adding certificate verification is strongly advised.
    See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
"""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

activities = []
access_token = ""


def auththorize():
    global access_token

    if config.strava_access_token:
        utils.log("Found saved access token. Skipping authorization")
        access_token = config.strava_access_token
        return

    try:
        response = requests.post(
            config.strava["auth_url"],
            data={
                "client_id": config.strava_client_id,
                "client_secret": config.strava_client_secret,
                "code": config.strava_authorization_code,
                "grant_type": "authorization_code",
                "f": "json",
            },
            verify=False,
        )
        access_token = response.json()["access_token"]
        utils.log("Authorization success. Your current access token: ", access_token)
    except Exception as e:
        utils.handle_error("Request error.", e)


def check_for_strava_activities_list():
    if not os.path.exists(config.strava["activities_list_file_path"]):
        utils.handle_error(
            f"{config.strava['activities_list_file_path']} does not exist."
        )


def load_actvities():
    global activities
    activities = utils.read_json_file(config.strava["activities_list_file_path"])


def upload_activities():
    try:
        for index, activity in enumerate(activities):
            file_path = config.common["gpx_file_path"].format(activity["external_id"])
            file_name = f"{activity['external_id']}.gpx"
            with open(file_path, "rb") as file:
                response = requests.post(
                    url=config.strava["upload_activites_url"],
                    headers={
                        "Accept": "application/json",
                        "Authorization": f"Bearer {access_token}",
                    },
                    data=activity,
                    files={
                        "file": (file_name, file, "application/gpx+xml"),
                    },
                )
                response.raise_for_status()
                utils.log(
                    f"[{index + 1}/{len(activities)}] ID: '{activity['external_id']}' Name: '{activity['name']}' activity uploaded."
                )
                utils.throttle_requests()
    except Exception as e:
        utils.handle_error("Request error.", e)


if __name__ == "__main__":
    utils.log("Running the script...")

    check_for_strava_activities_list()

    utils.log("Authorizing...")

    auththorize()

    utils.log("Uploading activites to Strava...")

    load_actvities()
    upload_activities()

    utils.log("Success. Activities have been uploaded to Strava.")
