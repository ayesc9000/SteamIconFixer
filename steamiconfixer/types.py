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

# Stores an icon's steam id, file path, and file name
class Icon:
    def __init__(self, steamid, path, name, shortcutfilename):
        self.steamid = steamid
        self.path = path
        self.name = name
        self.shortcutfilename = shortcutfilename
