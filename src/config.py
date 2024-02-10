"""
    AUTH
    * komoot_user_id - your Komoot user id - number, obtained from https://www.komoot.com/account/details
    * client_id - your client id - integer/string, obtainted from https://www.strava.com/settings/api
    * client_secret - your client secret - string, obtainted from https://www.strava.com/settings/api
    * authorization_code - your authorization code - string, in your browser go to this url:
      https://www.strava.com/oauth/authorize?client_id=[CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:write
      and then after the redirect extract the code from the link:
      http://localhost/exchange_token?state=&code=[HERE_IS_THE_CODE]&scope=read,activity:write
"""
komoot_user_id = 0
strava_client_id = ""
strava_client_secret = ""
strava_authorization_code = ""
strava_access_token = ""

common = {
    "enable_logs": True,
    "enable_logs_timestamp": True,
    "gpx_file_path": "../data/{}.gpx",
}

komoot = {
    "first_tours_lists_page_url": (
        "https://www.komoot.com/api/v007"
        f"/users/{komoot_user_id}/tours"
        "/?type=tour_recorded"
        "&sort_field=date"
        "&sort_direction=desc"
        "&status=public"
        "&page=0"
        "&limit=50"
    ),
    "tours_list_file_path": "../data/komoot-tours.json",
    "gpx_file_url": "https://www.komoot.com/api/v007/tours/{}.gpx",
    "save_only_wanted_keys": True,
    "wanted_keys": (
        "status",
        "type",
        "date",
        "name",
        "distance",
        "duration",
        "sport",
        "kcal_active",
        "kcal_resting",
        "elevation_up",
        "elevation_down",
        "time_in_motion",
        "id",
        "changed_at",
    ),
}

strava = {
    "auth_url": "https://www.strava.com/oauth/token",
    "upload_activites_url": "https://www.strava.com/api/v3/uploads",
    "activities_list_file_path": "../data/strava-activities.json",
}

"""
    Source:
    - from: https://static.komoot.de/doc/external-api/v007/sports.html
    - to: https://developers.strava.com/docs/uploads/
"""
komoot_to_strava_sport_type_map = {
    "hike": "Hike",
    "racebike": "Ride",
    # "e_racebike": "",
    "touringbicycle": "Ride",
    # "e_touringbicycle": "",
    "mtb": "MountainBikeRide",
    # "e_mtb": "",
    "mtb_easy": "GravelRide",
    # "e_mtb_easy": "",
    # "mtb_advanced": "",
    # "e_mtb_advanced": "",
    "jogging": "Run",
    # "climbing": "",
    # "downhillbike": "",
    # "nordic": "",
    # "nordicwalking": "",
    # "skaten": "",
    # "skialpin": "",
    # "skitour": "",
    # "sled": "",
    # "snowboard": "",
    # "snowshoe": "",
    # "unicycle": "",
    "citybike": "Ride",
    # "other": "",
}
