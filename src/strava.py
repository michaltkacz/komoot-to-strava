import requests
import sys
import urllib3
import json
import time

"""
    Hotfix for:
    InsecureRequestWarning: Unverified HTTPS request is being made to host 'www.strava.com'. 
    Adding certificate verification is strongly advised.
    See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
"""
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
    LINKS
"""
auth_url = "https://www.strava.com/oauth/token"
activities_url = "https://www.strava.com/api/v3/uploads"

"""
    CONFIG
    * client_id - obtainted from https://www.strava.com/settings/api
    * client_secret - obtainted from https://www.strava.com/settings/api
    * authorization_code:
    in browser go to this url:
    https://www.strava.com/oauth/authorize?client_id=[CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:write
    and then:
    http://localhost/exchange_token?state=&code=[HERE_IS_THE_CODE]&scope=read,activity:write
    extract the code from the link
"""
client_id = ""  # your client id - integer/string
client_secret = ""  # your client secret - string
authorization_code = ""  # your authorization code - string

"""
    FUNCTIONS
"""


def get_access_token():
    print("<< --- AUTHORIZE ---")
    print("Sending request...")
    response = requests.post(
        auth_url,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": authorization_code,
            "grant_type": "authorization_code",
            "f": "json",
        },
        verify=False,
    )
    if not response.ok:
        print("<< Bad response. Program will exit")
        sys.exit()
    print("<< Response OK. Processing data...")
    return response.json()["access_token"]


def load_actvities():
    file = open("./gpx/tours.json", "r")
    activities_raw = json.loads(file.read())
    activities = list(
        map(
            lambda a: {
                "external_id": a.get("id", None),
                "name": a.get("name", None),
                "file": open("./gpx/{}.gpx".format(a.get("id", "")), "rb"),
                "data_type": "gpx",
            },
            activities_raw,
        )
    )
    return activities


def upload_activities(activities, access_token):
    print("<< --- UPLOAD ACTIVITIES ---")
    for activity in activities:
        print("<< Sending request...")
        response = requests.post(
            activities_url,
            headers={"Authorization": "Bearer {}".format(access_token)},
            files={
                "activity_type": (None, "ride"),
                "trainer": (None, "0"),
                "commute": (None, "0"),
                "data_type": (None, "gpx"),
                "name": (None, activity.get("name", None)),
                "external_id": (None, activity.get("external_id", None)),
                "file": (
                    "{}.gpx".format(activity.get("external_id", None)),
                    activity.get("file", None),
                ),
            },
        )
        if not response.ok:
            print("<< Bad response. Program will exit")
            sys.exit()

        print("<< Response OK. Activity uploaded")
        time.sleep(1)


"""
    MAIN
"""
if __name__ == "__main__":
    access_token = get_access_token()
    activities = load_actvities()
    upload_activities(activities, access_token)
