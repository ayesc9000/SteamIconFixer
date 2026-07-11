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

import gi
import io
import os
import re
import subprocess
import traceback

from pathlib import Path
from PIL import Image
from steam.client import SteamClient
from steam.enums.emsg import EMsg
from termcolor import cprint
from ..types import Icon

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

steamapi = SteamClient()
gtk_sizes = [16, 32, 48, 64, 128, 256, 512, 1024, 2048]
gtk_user_path = os.path.expandvars('$HOME/.local/share/icons/hicolor')
gtk_icon_theme = Gtk.IconTheme.get_default()

usage = """Usage:
python sif.pyz <path to shortcuts directory> [path to icons directory]

Examples:
python sif.pyz ~/Desktop
python sif.pyz ~/Desktop/Steam Games
python sif.pyz ~/.local/share/applications
python sif.pyz ~/.local/share/applications $HOME/.icons
python sif.pyz /usr/share/applications/ /usr/share/pixmaps
"""

def initialize():
    print("Starting Steam client...")
    steamapi.anonymous_login()

def refresh_icon_cache():
    print("Refreshing the GTK icon cache, this might take a moment...")
    Path(gtk_user_path).touch()
    result = subprocess.run(["gtk-update-icon-cache"])

    if result.returncode != 0:
        cprint("Failed to update the icon cache. Try executing 'gtk-update-icon-cache' in another terminal for more information.", "red")
        return False
    return True

def setup_icon_storage_path(icon_storage):
    # Empty path signifies use Gtk icon paths
    if not len(icon_storage) == 0 and not os.path.exists(icon_storage):
        os.makedirs(icon_storage)

def is_shortcut(file):
    return file.name.endswith(".desktop")

def read_shortcut(file):
    with open(file, "r") as file:
        # Read contents and check if it is a valid desktop shortcut file
        contents = file.read()
        isvalid = re.search(r"\[Desktop Entry\]\n", contents)

        if isvalid is None:
            cprint(file.name + ": File is not a valid shortcut. Skipping.", "yellow")
            return None

        # Get the Steam ID and icon path
        steamidmatch = re.search(r"steam:\/\/rungameid\/([^\n]*)\n", contents)
        iconpathmatch = re.search(r"Icon=([^\n]*)\n", contents)

        if steamidmatch is None or iconpathmatch is None:
            cprint(file.name + ": Shortcut doesn't appear to be a Steam shortcut. Skipping.", "blue")
            return None

        steamid = steamidmatch.group(1)
        iconpath = iconpathmatch.group(1)

        # Check if the icon exists
        if iconpath == "steam":
            pass
        elif not Path(iconpath).is_absolute():
            # Ex: "steam_icon_440" can be valid as long as "steam_icon_440.png" exists within a valid icon search directory
            if gtk_icon_theme.has_icon(iconpath):
                cprint(file.name + ": Icon is present, nothing needs to be done.", "green")
                return None
        elif os.path.exists(iconpath):
            # Absolute icon paths to anywhere are also valid, however certain directories are recommended, such as $HOME/.icons
            if os.path.isfile(iconpath):
                cprint(file.name + ": Icon is present, nothing needs to be done.", "green")
                return None
            else:
                cprint(file.name + ": Icon path is a directory. This error must be fixed manually.", "red")
                return None

        # Fetch icon file name from the Steam API
        try:
            appinfo = steamapi.get_product_info(apps=[int(steamid)])
            iconname = appinfo["apps"][int(steamid)]["common"]["clienticon"] + ".ico"
        except Exception as exception:
            cprint("Could not fetch icon file name from the Steam API.", "red")
            traceback.print_exc()
            return None

        # Create an icon object and place it into the icon collection
        print(file.name + ": Icon is missing and will be redownloaded.")
        return Icon(steamid, iconpath, iconname, file)

def write_icon(icon, response, icon_storage):
    # Empty icon_storage means use GTK icons
    img = Image.open(io.BytesIO(response.content))
    
    if len(icon_storage) == 0:
        name = "steam_icon_" + icon.steamid
        width, height = img.size
        
        for x in gtk_sizes:
            if width < x and height < x:
                break
            
            full_dir = os.path.join(gtk_user_path, str(x) + "x" + str(x) + "/apps")
            if not os.path.exists(full_dir):
                os.makedirs(full_dir)
            
            thumb = img.copy()
            thumb.thumbnail((x, x), Image.LANCZOS)
            thumb.save(os.path.join(full_dir, name + ".png"), "PNG")
        
        return name
    else:
        savepath = Path(os.path.join(icon_storage, "steam_icon_" + icon.steamid + ".png")).resolve()
        img.save(savepath, "PNG")
        return str(savepath)

def update_shortcuts(icon, write_path):
    # Opening the same file twice, not ideal. Perhaps open in read/write and seek back to
    # the start to write the contents?
    with open(icon.shortcutfilename, "r") as file:
        contents = file.read()
        contents = re.sub(r"Icon=([^\n]*)\n", "Icon=" + write_path + "\n", contents)
    with open(icon.shortcutfilename, "w") as file:
        file.write(contents)
