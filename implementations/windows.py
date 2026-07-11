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

from termcolor import cprint
from ..types import Icon

usage = """Usage:
python sif.pyz <path to folder>

Examples:
python sif.pyz C:\\Users\\user\\Desktop
python sif.pyz "C:\\Users\\user\\Desktop\\Steam Games"
python sif.pyz "C:\\Users\\user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Steam"
"""

def initialize():
    # Unused on Windows
    pass

def refresh_icon_cache():
    # Unused on Windows
    return True

def setup_icon_storage_path(icon_storage):
    # Unused on Windows
    pass

def is_shortcut(file):
    return file.name.endswith(".url")

def read_shortcut(file):
    with open(file, "r") as file:
        # Read contents and check if it is a valid internet shortcut file
        contents = file.read()
        isvalid = re.search(r"\[InternetShortcut\]\n", contents)

        if isvalid is None:
            cprint(file.name + ": File is not a valid shortcut. Skipping.", "yellow")
            return None

        # Get the Steam ID, icon path, and icon file name
        steamidmatch = re.search(r"steam:\/\/rungameid\/([^\n]*)\n", contents)
        iconpathmatch = re.search(r"IconFile=([^\n]*)\n", contents)
        iconnamematch = re.search(r"\\([^\n\\]*)\n", contents)

        if steamidmatch is None or iconpathmatch is None or iconnamematch is None:
            cprint(file.name + ": Shortcut doesn't appear to be a Steam shortcut. Skipping.", "blue")
            return None

        steamid = steamidmatch.group(1)
        iconpath = iconpathmatch.group(1)
        iconname = iconnamematch.group(1)

        # Check if the icon exists
        if os.path.exists(iconpath):
            if not os.path.isfile(iconpath):
                cprint(file.name + ": Icon path is a directory. This error must be fixed manually.", "red")
                return None
            else:
                cprint(file.name + ": Icon is present, nothing needs to be done.", "green")
                return None

        # Create an icon object and place it into the icon collection
        print(file.name + ": Icon is missing and will be redownloaded.")
        return Icon(steamid, iconpath, iconname, file)

def write_icon(icon, response, icon_storage):
    with open(icon.path, "wb") as file:
        file.write(response.content)
    return icon.path

def update_shortcuts(icon, write_path):
    # Unused on Windows
    return None
