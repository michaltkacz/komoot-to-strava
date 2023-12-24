# user_id: integer - your komoot user ID
komoot_user_id = 0

common = {
    "tours_data_directory": "../data/",
    "tours_list_file_name": "tours",
    "tours_list_file_extension": ".json",
    "gpx_file_extension": ".gpx",
    "file_name_safe_separator": "___",
}

komoot = {
    "first_page_url": (
        "https://www.komoot.com/api/v007"
        f"/users/{komoot_user_id}/tours"
        "/?type=tour_recorded"
        "&sort_field=date"
        "&sort_direction=desc"
        "&status=public"
        "&page=0"
        "&limit=50"
    ),
    "gpx_file_url": "https://www.komoot.com/api/v007/tours/{}.gpx",
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
