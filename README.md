# Komoot To Strava Data Importer

> Python scripts for transferring cycling activities from _Komoot_ to _Strava_

## Table of contents

- [Komoot Routes](#komoot-routes)
  - [Table of contents](#table-of-contents)
  - [General info](#general-info)
  - [Setup and run](#setup-and-run)
  - [Important notes](#important-notes)
  - [Contact](#contact)

## General info

This repository contains two Python scripts:

- komoot.py - download activities data and GPX files from your _Komoot_ account. This script is a little bit tricky, because it uses _Komoot_ API endpoint without any authorization. Thus, it can download data only of public activities and only from public accounts. Also the "Privacy zones" should be disabled for the time of script run, otherwise the downloaded GPX files will be truncated by these zones. Activitiy details are saved to `./gpx/tours.json` file ane GPX files to `./gpx/{TOUR_ID}.gpx`.
- strava.py - upload activities to your _Strava_ account. This script uses authorization, also in a kind of tricky way. In order to use it, you have to [register own _Strava_ API application](https://developers.strava.com/docs/getting-started/#account) and obtain `client id`, `client secret` and `access token` with `activity:write` scope.

I wrote these scripts for my personal, one-time use, therefore they are full of _hacks_ and they are basically quite janky, however - for me - they did the job. This readme will serve me as a future reminder in case, I would like to use it again.

## Setup and run

Scripts were developed with Python v3.9.4.

### Komoot

1. Make sure that your profile is public, all your tours all public and your privacy zones are disabled. You can switch them back after the export.
2. Go to `Settings > Account > User ID` and copy your user ID.
3. Open komoot.py file and assign your user ID to the variable `user_id`.
   ```python
       """
           CONFIG
           * user_id - your komoot user ID
       """
       user_id = 0 # your user ID here - integer
   ```
4. Go to `src` directory and run komoot.py from the terminal.
   ```
      ./komoot.py
   ```
5. Wait until script will finish.

### Strava

1. [Register own _Strava_ API application.](https://developers.strava.com/docs/getting-started/#account)
2. In your browser go to the given address. Change `[CLIENT_ID]` to your client ID:

   https://www.strava.com/oauth/authorize?client_id=[CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:write

3. Authorize with your _Strava_ account and wait for redirect (it will redirect you to the page, that doesn't exist - it's ok).
4. After redirect, copy `code` (that is `authorization code`) from the address:

   http://localhost/exchange_token?state=&code=[HERE_IS_THE_CODE_TO_COPY]&scope=read,activity:write

5. Now paste `client id`, `client secret` amd `authorization code` in the strava.py file.
   ```python
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
   client_id = "" # your client id - integer/string
   client_secret = "" # your client secret - string
   authorization_code = "" # your authorization code - string
   ```
6. Go to `src` directory and run strava.py from the terminal.
   ```
      ./strava.py
   ```
7. Wait until script will finish.

## Important notes

- **Strava API allows to up to 100 calls every 15 minutes and up to 1000 calls every day. Every uploaded activity is equal to one call, so if you want to upload more than 100 activities, you have to split them in smaller chunks.**
- **In case of: missing files, unexpected errors, bad API calls, etc. the scripts will most likely just stop working.**
- **You might need to manually create `gpx` folder in `src` folder before running scripts**

## Contact

Created by [@michaltkacz](https://github.com/michaltkacz) - feel free to contact me!
