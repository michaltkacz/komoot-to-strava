# Komoot To Strava Data Importer

> Python scripts for transferring tours from _Komoot_ to _Strava_ activities.

## General info

The whole script is divided into four parts:
1. `komoot-get-tours.py`
2. `komoot-get-gpx.py`
3. `komoot-to-strava-mapper.py`
4. `strava-upload-activites.py`

plus `config.py` for configuration and `utils.py` for common functions.

`komoot-get-tours.py` and `komoot-get-gpx.py` download activities data and GPX files from your _Komoot_ account. This script is a little bit tricky because it uses _Komoot_ API endpoint without any authorization. Thus, it can download data only from **public activities** and only from **public accounts**. Also **the "Privacy zones" must be disabled** for the time of script run, otherwise, the downloaded GPX files will be truncated by these zones. Komoot tours data by default is saved to `./data/komoot-tours.json` file and GPX files to `./data/{TOUR_ID}.gpx`.

`komoot-to-strava-mapper.py` maps data saved in `./data/komoot-tours.json` to a model required for uploading activity to Strava. Output is saved by default in `./data/strava-activities.json`

`strava-upload-activies.py` - upload activities to your _Strava_ account. This script uses authorization, also in a kind of tricky way. To use it, you have to [register own _Strava_ API application](https://developers.strava.com/docs/getting-started/#account) and obtain `client id`, `client secret`, `authorization code` and `access token` with `activity:write` scope.


I wrote the script for my personal, one-time use, therefore it is generally quite janky, however - for me - it did the job (though it turned out that I wanted to use it again after some time, so I rewrote most of the code - still janky).

## Setup and run

Scripts were developed with `python3`.

### Get tours from Komoot

1. Make sure that your [profile is public](https://support.komoot.com/hc/en-us/articles/360023355191-Managing-your-profile-visibility), all your [tours all public](https://support.komoot.com/hc/en-us/articles/360023355331-Controlling-who-sees-your-Tours) and your [privacy zones are disabled](https://support.komoot.com/hc/en-us/articles/360046595312-Privacy-Zones). You can easily switch them back after the export.
2. Go to the `Settings > Account > User ID` and copy your user ID.
3. Open the `config.py` file and paste your user ID to the variable the `komoot_user_id` as a number:
   ```python
      komoot_user_id = 012345679
   ```
4. Go to the `./src` directory and run the `komoot-get-tours.py` from the terminal:
   ```
      $ cd src
      $ python3 komoot-get-tours.py
   ```
5. Wait until the script finishes.
6. Run the `komoot-get-gpx.py` from the terminal:
   ```
      $ cd src
      $ python3 komoot-get-gpx.py
   ```
6. Wait until the script finishes.
7. You can now switch back your privacy settings to more private and bring back 'Privacy zones'.

### Map Komoot tours data to Strava activities data
1. Go to the `./src` directory and run `komoot-to-strava-mapper.py` from the terminal:
   ```
      $ cd src
      $ python3 komoot-to-strava-mapper.py
   ```
2. Wait until the script finishes.

### Strava

1. [Register your own _Strava_ API application.](https://developers.strava.com/docs/getting-started/#account)
2. Using [this instruction](https://developers.strava.com/docs/getting-started/#oauth:~:text=For%20demonstration%20purposes%20only%2C%20here%20is%20how%20to%20reproduce%20the%20graph%20above%20with%20cURL) get your `authorization code`:
   1. In your browser go to the given address. Change the `[CLIENT_ID]` to your client ID:
   https://www.strava.com/oauth/authorize?client_id=[CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:write
   2. Authorize with your _Strava_ account and wait for redirect (it will redirect you to the page, that doesn't exist - it's ok).
   3. After the redirect, copy the `code` (which is your `authorization code`) from the address:
   http://localhost/exchange_token?state=&code=[HERE_IS_THE_CODE_TO_COPY]&scope=read,activity:write

3. Now paste the `client id`, `client secret` (both from your [application page](https://www.strava.com/settings/api)) and the `authorization code` (copied from the previous step) in the `config.py` file:
   ```python
   """
   strava_client_id = "<client id>"
   strava_client_secret = "<client secret>"
   strava_authorization_code = "<authorization code>"
   strava_access_token = "" # see the note below
   ```
4. Go to the `./src` directory and run `strava-upload-activities.py` from the terminal:
   ```
      $ cd src
      $ python3 strava-upload-activities.py
   ```
5. Wait until the script finishes.

Note: after the first `strava-upload-activities.py` script run you will receive your `access token` and your `authorization code` becomes invalid. The access token has a long expiration time. So to avoid the need for authorization of every script run, you can copy your `access token` (it will be printed in the console on the first run) and paste it to `conifg.py` file under the `strava_access_token` variable.

## Important notes

- [Strava has API limits](https://developers.strava.com/docs/rate-limits/#:~:text=Strava%20API%20usage%20is%20limited,may%20need%20to%20be%20adjusted.). Every uploaded activity is equal to one call, so if you want to upload a lot of activities, you might need to manually split them into smaller chunks and spread uploading in time. The easiest way to do it would be to manually edit the `strava-activities.json` file - just cut out a chunk of activities, and back it up in another file. Upload the current chunk and then replace the data.
- In case of missing files, already existing files, unexpected errors, bad API calls, etc. the scripts will most likely just stop working.
- You might need to manually create an empty `data` folder before running scripts.
- You can adjust the config in the `config.py` file, including the sport types map:
   - [Komoot](https://static.komoot.de/doc/external-api/v007/sports.html)
   - [Strava](https://developers.strava.com/docs/uploads/)
