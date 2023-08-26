# Steam Icon Fixer, Version 1.0
# Copyright (C) 2023 Liam "AyesC" Hogan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

import os
import re
import requests
import sys

from termcolor import colored

icons = {}
baseurl = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/"

license = """\nSteam Icon Fixer, Version 1.0
Copyright (C) 2023 Liam "AyesC" Hogan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/."""

usage = """---------------------------------------------

Usage:
sif.exe <path to file>

Examples:
sif.exe C:\\Users\\user\\Desktop
sif.exe "C:\\Users\\user\\Desktop\\Steam Games"
sif.exe "C:\\Users\\user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Steam"

Errors & Exit Codes:
<path> does not exist. (exit code 1): The specified directory does not exist.
<path> is a file. (exit code 2): The specified path is not a directory.
"""

# Stores an icon's steam id, file path, and file name
class Icon:
    def __init__(self, steamid, path, name):
        self.steamid = steamid
        self.path = path
        self.name = name

# Print license
print(license + "\n\n")

# This program only works on Windows
if not os.name == "nt":
    print(colored("This program is not compatible with your operating system. You may only run this program on a Windows system.", "red"))

# Validate arguments
if len(sys.argv) < 2:
    print(usage)
    sys.exit(0)

searchpath = sys.argv[1]

if not os.path.exists(searchpath):
    print(colored(searchpath + " does not exist.", "yellow"))
    sys.exit(1)

if os.path.isfile(searchpath):
    print(colored(searchpath + " is a file.", "yellow"))
    sys.exit(2)

# Create list of icons
print("Searching for valid Steam shortcuts in " + searchpath + "...")

for filename in os.scandir(searchpath):
    # Igore directories or any files that are not .url files
    if not filename.is_file():
        continue

    if not filename.name.endswith(".url"):
        continue

    try:
        with open(filename, "r") as file:
            # Read contents and check if it is a valid internet shortcut file
            contents = file.read()
            isvalid = re.search(r"\[InternetShortcut\]\n", contents)

            if isvalid == None:
                print(colored(filename.name + ": File is not a valid internet shortcut. Skipping.", "red"))
                continue

            # Get the Steam ID, icon path, and icon file name
            steamidmatch = re.search(r"rungameid\/([^\n]*)\n", contents)
            iconpathmatch = re.search(r"IconFile=([^\n]*)\n", contents)
            iconnamematch = re.search(r"\\([^\n\\]*)\n", contents)

            if steamidmatch == None or iconpathmatch == None or iconnamematch == None:
                print(colored(filename.name + ": Shortcut doesn't appear to be a Steam shortcut. Skipping.", "yellow"))
                continue

            steamid = steamidmatch.group(1)
            iconpath = iconpathmatch.group(1)
            iconname = iconnamematch.group(1)

            # Check if the icon exists
            if os.path.exists(iconpath):
                if not os.path.isfile(iconpath):
                    print(colored(filename.name + ": Icon path is a directory. This error must be fixed manually. Skipping.", "red"))
                    continue
                else:
                    print(colored(filename.name + ": Icon file is present, nothing needs to be done. Skipping.", "green"))
                    continue

            # Create an icon object and place it into the icon collection
            icons[steamid] = Icon(steamid, iconpath, iconname)
            print(colored(filename.name + ": Icon missing, valid Steam game. Will be redownloaded.", "yellow"))
    except Exception as error:
        print(colored(filename.name + ": Could not open the file. Make sure it's not in use and it's permissions are set correctly. Skipping.", "red"))
        print(error.with_traceback())
        continue

print("")

# Check if there are icons to redownload
if len(icons) < 1:
    print("No icons need to be redownloaded. Refer to the log above for any errors.")
    sys.exit(0)

# Print the results and ask for user confirmation
print("Found " + str(len(icons)) + " missing icons.")
print("Do you want to redownload the icons? (y/N): ", end="")

choice = input().lower()

print("")

if not choice == "y":
    print(colored("Cancelled.", "red"))
    sys.exit(0)

# Download the icons
print("Downloading " + str(len(icons)) + " icons...")

errors = 0

for steamid, icon in icons.items():
    # Create the URL and make a request
    url = baseurl + steamid + "/" + icon.name
    response = requests.get(url)

    # Check if response was ok
    if not response.ok:
        print(colored(steamid + ": Failed to download icon. Response code was " + response.status_code + ".", "red"))
        errors = errors + 1
        continue

    # Write the downloaded icon to disk
    try:
        with open(icon.path, "wb") as file:
            file.write(response.content)
    except:
        print(colored(steamid + ": Failed to write the icon to disk.", "red"))
        errors = errors + 1
        continue

    print(colored(steamid + ": Downloaded and saved successfully.", "green"))

print("\nDownloading completed with " + str(errors) + " errors. Refer to the above log for details.")
