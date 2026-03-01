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

from termcolor import colored

from ..types import Icon

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
Incompatible operating system (exit code 100)
"""

def isshortcut(filename):
    return filename.name.endswith(".url")

def setupiconpath(filename):
    return ""

def readshortcut(filename):
    with open(filename, "r") as file:
        # Read contents and check if it is a valid internet shortcut file
        contents = file.read()
        isvalid = re.search(r"\[InternetShortcut\]\n", contents)

        if isvalid == None:
            print(colored(filename.name + ": File is not a valid internet shortcut. Skipping.", "red"))
            return None

        # Get the Steam ID, icon path, and icon file name
        steamidmatch = re.search(r"steam:\/\/rungameid\/([^\n]*)\n", contents)
        iconpathmatch = re.search(r"IconFile=([^\n]*)\n", contents)
        iconnamematch = re.search(r"\\([^\n\\]*)\n", contents)

        if steamidmatch == None or iconpathmatch == None or iconnamematch == None:
            print(colored(filename.name + ": Shortcut doesn't appear to be a Steam shortcut. Skipping.", "yellow"))
            return None

        steamid = steamidmatch.group(1)
        iconpath = iconpathmatch.group(1)
        iconname = iconnamematch.group(1)

        # Check if the icon exists
        if os.path.exists(iconpath):
            if not os.path.isfile(iconpath):
                print(colored(filename.name + ": Icon path is a directory. This error must be fixed manually. Skipping.", "red"))
                return None
            else:
                print(colored(filename.name + ": Icon file is present, nothing needs to be done. Skipping.", "green"))
                return None

        # Create an icon object and place it into the icon collection
        print(colored(filename.name + ": Icon missing, valid Steam game. Will be redownloaded.", "yellow"))
        return Icon(steamid, iconpath, iconname, filename)

def writeicon(icon, response, iconpath):
    with open(icon.path, "wb") as file:
        file.write(response.content)
    return icon.path

def updateshortcuts(icon, searchpath, iconpath):
    return None
