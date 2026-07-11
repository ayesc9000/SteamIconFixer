# Steam Icon Fixer
# Copyright (C) 2023, 2026 Liam "AyesC" Hogan and contributors
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
import traceback

from termcolor import cprint
from implementations import detector

banner = """\nSteam Icon Fixer
Copyright (C) 2023, 2026 Liam "AyesC" Hogan and contributors.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/.\n\n"""
baseurls = [
    "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/",
    "https://shared.fastly.steamstatic.com/community_assets/images/apps/",
    ]
exit_codes = """\n\nExit codes:
-1: Platform not supported.
-2: Invalid usage.
-3: Invalid path or file specified.
-4: Failure refreshing GTK icon cache."""
icons = {}

print(banner)

# Get implementation of platform-specific functions
implementation = detector.get_implementation()
if implementation is None:
    cprint("This program is not compatible with your operating system. Supported platforms: " + detector.platform_names + ".", "red")
    sys.exit(-1)

# Validate arguments
arglen = len(sys.argv)
if arglen < 1 or arglen > 2:
    print(implementation.usage + exit_codes)
    sys.exit(-2)

searchpath = sys.argv[1]
iconpath = ""

if arglen == 2:
    iconpath = sys.argv[2]

# not the cleanest way of doing this
if not os.path.exists(searchpath):
    cprint(searchpath + " does not exist.", "red")
    sys.exit(-3)

if os.path.isfile(searchpath):
    cprint(searchpath + " is a file.", "red")
    sys.exit(-3)

if not iconpath == "":
    if not os.path.exists(iconpath):
        cprint(iconpath + " does not exist.", "red")
        sys.exit(-3)
    
    if os.path.isfile(iconpath):
        cprint(iconpath + " is a file.", "red")
        sys.exit(-3)

# Create list of icons
if not implementation.refresh_icon_cache():
    sys.exit(-4)

print("Searching for valid Steam shortcuts in " + searchpath + "...")
for filename in os.scandir(searchpath):
    # Igore directories or any files that are not shortcuts.
    if not filename.is_file():
        continue

    if not implementation.is_shortcut(filename):
        continue

    try:
        iconobj = implementation.read_shortcut(filename)
        if iconobj is not None:
            icons[iconobj.steamid] = iconobj
    except Exception as error:
        cprint(filename.name + ": Could not open the file. Make sure it's not in use and it's permissions are set correctly. Skipping.", "red")
        traceback.print_exc()
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

iconpath = detector.setupiconpath(iconpath)

# Download the icons
print("Downloading " + str(len(icons)) + " icons...")

errors = 0

current_baseurl_index = 0
current_baseurl = baseurls[current_baseurl_index]

for steamid, icon in icons.items():
    # Create the URL and make a request
    url = current_baseurl + steamid + "/" + icon.name
    response = requests.get(url)

    while not response.ok:
        print(colored("Got code " + str(response.status_code) + " at CDN " + current_baseurl, "red"))
        current_baseurl_index = current_baseurl_index + 1
        if current_baseurl_index < len(baseurls):
            current_baseurl = baseurls[current_baseurl_index]
            print(colored("Retrying with CDN " + current_baseurl, "red"))
            url = current_baseurl + steamid + "/" + icon.name
            response = requests.get(url)
        else:
            print(colored("All CDNs failed to respond", "red"))
            sys.exit(0)

    # Check if response was ok
    if not response.ok:
        print(colored(steamid + ": Failed to download icon. Response code was " + str(response.status_code) + ".", "red"))
        errors = errors + 1
        continue

    # Write the downloaded icon to disk
    try:
        writepath = detector.writeicon(icon, response, iconpath)
    except Exception as error:
        print(colored(steamid + ": Failed to write the icon to disk.", "red"))
        traceback.print_exc()
        errors = errors + 1
        continue
    
    try:
        detector.updateshortcuts(icon, searchpath, writepath)
    except Exception as error:
        print(colored(steamid + ": Failed to update application shortcut", "red"))
        traceback.print_exc()
        errors = errors + 1
        continue

    print(colored(steamid + ": Downloaded and saved successfully.", "green"))

print("\nDownloading completed with " + str(errors) + " errors. Refer to the above log for details.")

detector.refreshiconcache()
