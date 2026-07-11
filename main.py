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
cdns = [
    "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/",
    "https://shared.fastly.steamstatic.com/community_assets/images/apps/",
]
exit_codes = """\n\nExit codes:
0: No issues.
-1: Platform not supported.
-2: Invalid usage.
-3: Invalid path or file specified.
-4: Failure refreshing GTK icon cache.
-5: Failure setting up icon storage directory.
-6: Rate-limited by CDNs or Steam during download."""
icons = []

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

search_path = sys.argv[1]
icon_storage = ""

if arglen == 2:
    icon_storage = sys.argv[2]

# not the cleanest way of doing this
if not os.path.exists(search_path):
    cprint(search_path + " does not exist.", "red")
    sys.exit(-3)

if os.path.isfile(search_path):
    cprint(search_path + " is a file.", "red")
    sys.exit(-3)

if not icon_storage == "":
    if not os.path.exists(icon_storage):
        cprint(icon_storage + " does not exist.", "red")
        sys.exit(-3)
    
    if os.path.isfile(icon_storage):
        cprint(icon_storage + " is a file.", "red")
        sys.exit(-3)

# Create list of icons
implementation.initialize()
if not implementation.refresh_icon_cache():
    sys.exit(-4)

print("Searching for valid Steam shortcuts in " + search_path + "...")
for filename in os.scandir(search_path):
    # Igore directories or any files that are not shortcuts.
    if not filename.is_file():
        continue
    elif not implementation.is_shortcut(filename):
        continue

    try:
        icon = implementation.read_shortcut(filename)
        if icon is not None:
            icons.append(icon)
    except Exception as exception:
        cprint(filename.name + ": Could not open the shortcut file. Make sure it's not in use and it's permissions are set correctly.", "yellow")
        traceback.print_exc()
        continue

# If there are icons to download, ask the user to continue
if len(icons) < 1:
    print("\nThere are no icons to download. Refer to the log above for details.")
    sys.exit(0)

while True:
    print("\nThere are " + str(len(icons)) + " icons to download.")
    print("Do you want to continue? (y/N): ", end="")
    
    choice = input().lower()
    if choice == "n" or choice == "":
        sys.exit(0)
    elif choice == "y":
        break

# Download the icons
def get_request(icon, cdn):
    url = current_cdn + icon.steamid + "/" + icon.name
    return requests.get(url)

try:
    implementation.setup_icon_storage_path(icon_storage)
except Exception as exception:
    cprint("Could not set up the icon storage directory. Check the required permissions of the target directory.", "red")
    traceback.print_exc()
    sys.exit(-5)

errors = 0
cdn_index = 0
current_cdn = cdns[cdn_index]
print("\nDownloading " + str(len(icons)) + " icons...")

for icon in icons:
    # Get icon as a request
    response = get_request(icon, current_cdn)
    while not response.ok:
        if response.status_code == 429:
            cprint("This IP address is being rate-limited by CDN '" + current_cdn + "'", "red")
        else
            cprint("Request failed with code " + str(response.status_code) + " from CDN '" + current_cdn + "'", "red")
        
        cdn_index = cdn_index + 1
        if cdn_index > len(cdns):
            cprint("All CDNs have been exhaused. If you were being rate-limited, try again later.", "red")
            cprint("Note that the GTK icon cache may need to be refreshed.", "yellow")
            sys.exit(-6)
        
        current_cdn = cdns[cdn_index]
        print("Retrying with CDN " + current_cdn)
        response = get_request(icon, current_cdn)

    # Write the downloaded icon to disk
    try:
        write_path = implementation.write_icon(icon, response, icon_storage)
    except Exception as exception:
        cprint(icon.steamid + ": Failed to write the icon file to disk.", "red")
        traceback.print_exc()
        errors = errors + 1
        continue
    
    try:
        implementation.update_shortcuts(icon, write_path)
    except Exception as exception:
        cprint(icon.steamid + ": Failed to update shortcut file with new icon.", "red")
        traceback.print_exc()
        errors = errors + 1
        continue

    cprint(icon.steamid + ": Downloaded successfully.", "green")

implementation.refresh_icon_cache()

if errors > 0
    print("\nDownloading completed with " + str(errors) + " errors. Refer to the log above for details.")
else
    print("\nDownloading completed. Refer to the log above for details.")
