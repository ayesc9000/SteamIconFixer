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

import io
import os
import re

from termcolor import colored
from steam.client import SteamClient
from steam.enums.emsg import EMsg
from PIL import Image
from pathlib import Path

from ..types import Icon

usage = """---------------------------------------------

Usage:
sif <path to file> [path to icons]

Examples:
sif ~/Desktop
sif ~/Desktop/Steam Games
sif ~/.local/share/applications $HOME/.icons
sif /usr/share/applications/ /usr/share/pixmaps

Errors & Exit Codes:
<path> does not exist. (exit code 1): The specified directory does not exist.
<path> is a file. (exit code 2): The specified path is not a directory.
Incompatible operating system (exit code 100)
"""

steamapi = SteamClient()
steamapi.anonymous_login()

def isshortcut(filename):
    return filename.name.endswith(".desktop")

def setupiconpath(filename):
    if len(filename) == 0:
        filename = os.path.expandvars("$HOME/.icons")
    if not os.path.exists(filename):
        os.makedirs(filename)
    return filename

def readshortcut(filename):
    with open(filename, "r") as file:
        # Read contents and check if it is a valid desktop shortcut file
        contents = file.read()
        isvalid = re.search(r"\[Desktop Entry\]\n", contents)

        if isvalid == None:
            print(colored(filename.name + ": File is not a valid desktop shortcut. Skipping.", "red"))
            return None

        # Get the Steam ID, icon path, and icon file name
        steamidmatch = re.search(r"steam:\/\/rungameid\/([^\n]*)\n", contents)
        iconpathmatch = re.search(r"Icon=([^\n]*)\n", contents)

        if steamidmatch == None or iconpathmatch == None:
            print(colored(filename.name + ": Shortcut doesn't appear to be a Steam shortcut. Skipping.", "yellow"))
            return None

        steamid = steamidmatch.group(1)
        iconpath = iconpathmatch.group(1)

        # Check if the icon exists
        if iconpath != "steam" and os.path.exists(iconpath):
            if not os.path.isfile(iconpath):
                print(colored(filename.name + ": Icon path is a directory. This error must be fixed manually. Skipping.", "red"))
                return None
            else:
                print(colored(filename.name + ": Icon file is present, nothing needs to be done. Skipping.", "green"))
                return None

        # Fetch icon file name from Steam APi
        try:
            appinfo = steamapi.get_product_info(apps=[int(steamid)])
            iconname = appinfo["apps"][int(steamid)]["common"]["clienticon"] + ".ico"
        except Exception as error:
            print(colored("Could not fetch icon name from Steam API. Skipping.", "red"))
            print(error.with_traceback())
            return None

        # Create an icon object and place it into the icon collection
        print(colored(filename.name + ": Icon missing, valid Steam game. Will be redownloaded.", "yellow"))
        return Icon(steamid, iconpath, iconname, filename)

def writeicon(icon, response, iconpath):
    img = Image.open(io.BytesIO(response.content))
    savepath = Path(os.path.join(iconpath, "steamicon_" + Path(icon.name).stem + ".png")).resolve()
    img.save(savepath, "PNG")
    return str(savepath)

def updateshortcuts(icon, searchpath, iconpath):
    with open(icon.shortcutfilename, "r") as file:
        contents = file.read()
        contents = re.sub(r"Icon=([^\n]*)\n", "Icon=" + iconpath + "\n", contents)
    with open(icon.shortcutfilename, "w") as file:
        file.write(contents)
