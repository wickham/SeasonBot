#!/usr/bin/env python
import calendar, datetime
import getopt
import json
import shutil
import sys
import difflib

from pathlib import Path

__settings_default = "seasonSettings.json"
__json_default = {
    "season": "SPRING",
    "server_path": "/",
    "season_dir" : "SEASONS",
    "files_included": [
        "db/*",
        "env/*",
        "mod_ce/*",
        "SurvivorMissionModule/*",
        "areaflags.map",
        "cfgeconomycore.xml",
        "cfgEffectArea.json",
        "cfgenvironment.xml",
        "cfgeventgroups.xml",
        "cfgeventspawns.xml",
        "cfggameplay.json",
        "cfgignorelist.xml",
        "cfglimitsdefinition.xml",
        "cfglimitsdefinitionuser.xml",
        "cfgplayerspawnpoints.xml",
        "cfgrandompresets.xml",
        "cfgspawnabletypes.xml",
        "cfgweather.xml",
        "init.c",
        "mapclusterproto.xml",
        "mapgroupcluster.xml",
        "mapgroupcluster01.xml",
        "mapgroupcluster02.xml",
        "mapgroupcluster03.xml",
        "mapgroupcluster04.xml",
        "mapgroupcluster05.xml",
        "mapgroupdirt.xml",
        "mapgrouppos.xml",
        "mapgroupproto.xml",
    ],
    "files_ignored": ["storage_1/*"],
    "seasons" :[
        "SPRING",
        "SUMMER",
        "FALL",
        "WINTER"
    ],
    "generated": "date",
}


def generate_default_settings():
    with open("seasonSettings.json", "w") as json_file:
        new_json = __json_default
        new_json["generated"] = str(datetime.datetime.now())
        json.dump(__json_default, json_file, indent=4, sort_keys=False)


def move_files(settings_file="seasonSettings.json"):
    print("[move_files] - START")
    print(settings_file)

    with open(settings_file, "r") as json_file:
        json_data = json.load(json_file)
    print(json_data["server_path"])
    if json_data["server_path"] == "/" or "root" or "\\":
        print("Server path is set to root dir, fixing the absolute path")
        json_data["server_path"] = str(Path.cwd())
        print(json_data)

        with open(settings_file, "w") as json_file:
            json.dump(json_data, json_file, indent=4, sort_keys=False)
    return print("[move_files] - END")


def check_diff():
    d1 = "C:/Users/mynam/Documents/Code/SeasonBot/SEASONS/FALL"
    d2 = "C:/Users/mynam/Documents/Code/SeasonBot"
    file = "types.xml"

    with open(f"{d1}/{file}") as file_1:
        file_1_text = file_1.readlines()

    with open(f"{d2}/{file}") as file_2:
        file_2_text = file_2.readlines()

    # Find and print the diff:
    for line in difflib.unified_diff(
        file_1_text,
        file_2_text,
        fromfile=f"{d1}/{file}",
        tofile=f"{d2}/{file}",
        lineterm="",
    ):
        print(line)


def check_season(season, settings_given=None):
    """If season to check is current season set, return"""
    if settings_given is None:
        print(f"[ERROR] No Settings were given to check! Attempting default...")
        settings_given = __settings_default

    if not Path.is_file(Path.cwd() / settings_given):
        print(f'[ERROR] File does not exist: "{settings_given}"')
        print(f'[REPAIR] New "seasonSettings.json" file will now be generated...')
        generate_default_settings()

    print(Path.exists(Path.cwd() / settings_given))

    try:
        with open(settings_given, "r") as f:
            data = json.load(f)
    except:
        print(f'[ERROR] Settings given is invalid: "{settings_given}"')
        raise

    try:
        if data["season"] != season:
            print("New season!")
    
            # MOVE FILES OUT
            # MOVE FILES IN
            move_files(settings_given)

            with open(settings_given, "r") as json_file:
                data = json.load(json_file)

            data["season"] = season

            with open(settings_given, "w") as json_file:
                json.dump(data, json_file, indent=4, sort_keys=False)
        else:
            print("no change needed")
            return
    except:
        print("[ERROR] 'season' key not found in json file!")
        raise


def get_season(month=None, settings=None):
    table = {month: index for index, month in enumerate(calendar.month_abbr) if month}

    if (month is None) or not isinstance(month, str):
        month = table[datetime.date.today().strftime("%B")[:3].capitalize()]
    else:
        month = table[month[:3].capitalize()]

    # if ("/" or "\\" in settings) and not Path.is_file(str(settings)):
    #     print(f'[ERROR] 1File does not exist: "{settings}"')
    #     print("Defaulting to basic season generator...")
    #     return ["SPRING", "SUMMER", "FALL", "WINTER"][int(round((month % 12) / 3, 0)) - 1]
    if settings is None:
        print("Defaulting to basic season generator...")
        return ["SPRING", "SUMMER", "FALL", "WINTER"][int(round((month % 12) / 3, 0)) - 1]
    
    with open(settings, "r") as json_file:
        json_data = json.load(json_file)
    return json_data["seasons"][int(round((month % 12) / (12 / len(json_data["seasons"])), 0)) - 1]


def main(argv):
    """Main - A really dumb way to automate seasons"""
    try:
        options, args = getopt.getopt(argv, "m:s:", ["month=", "setting="])
    except getopt.getopt.GetoptError:
        print("season_bot.py -m <month_to_check> -s <setting.json>")

    month_given = None
    settings_given = None
    for option, arg in options:
        if option in ("-h", "--help"):
            print("season_bot.py -m <month> -s <setting.json>")
            sys.exit()
        elif option in ("-m", "--month"):
            month_given = arg
        elif option in ("-s", "--setting"):
            settings_given = str(arg)

    print(f"{month_given} | {settings_given}")

    if not argv:
        season = get_season()
    else:
        season = get_season(month_given, settings_given)

    print(season)
    if check_season(season, settings_given) is None:
        return

    # Done


if __name__ == "__main__":
    main(sys.argv[1:])
